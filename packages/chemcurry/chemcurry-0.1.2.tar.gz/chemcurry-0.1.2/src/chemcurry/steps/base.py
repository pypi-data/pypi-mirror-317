"""base classes and functions for curation steps"""

import abc
import hashlib
import inspect
import warnings
from copy import deepcopy
from typing import Any, List, Optional, Tuple

from rdkit.Chem import Mol

from ..molecule import Molecule


DEFAULT_ISSUE = "Unspecified issue flagged by {} step"
DEFAULT_NOTE = "Unspecified note flagged by {} step"


def check_for_boost_rdkit_error(error_message: str) -> bool:
    """
    Return True if TypeError message is a RDKit Boost Error

    This is because you cannot directly catch RDKit errors, but
    catching all errors could make resolving bugs harder.
    This function should help enable the identification of
    RDKit errors

    Notes
    -----
    This is not perfect, there is a possibility that a non-rdkit error
    can get caught since it just looks for text 'rdkit' and 'boost' in
    the error message. If you have a weird bug you cannot sort out it is
    worth taking a look and seeing if this is catching a error it should
    not be

    Parameters
    ----------
    error_message: str
        the error message as a string

    Returns
    -------
    bool
    """
    error_message = error_message.lower()
    return ("boost" in error_message) and ("rdkit" in error_message)


class CurationStepError(Exception):
    """
    Default exception to throw if there is an error raised with a CurationStep

    This should only be raised if there is an error that is caused by CurationStep itself.
    For example, the curation step lacks both a note and and issue message during instantiation.
    """

    pass


class NoteMixin:
    """Mixin for adding a note message to a BaseCurationStep object"""

    note: str = DEFAULT_NOTE.format(__name__)

    def get_note_text(self, *args) -> str:
        """
        Get the note as a str with rendered format

        Parameters
        ----------
        *args
            string format values to render into the note str
            must appear in order they appear in the note str

        Returns
        -------
        str
        """
        return self.note.format(*args)


class IssueMixin:
    """Mixin for adding a issue message to a BaseCurationStep object"""

    issue: str = DEFAULT_ISSUE.format(__name__)

    def get_issue_text(self, *args) -> str:
        """
        Get the issue as a str with rendered format

        Parameters
        ----------
        *args
            string format values to render into the issue str
            must appear in order they appear in the issue str

        Returns
        -------
        str
        """
        return self.issue.format(*args)


class PostInitMeta(abc.ABCMeta, type):
    """
    Enables a '__post_init__' hook that is called after '__init__'

    To help with error handling when defining new CurationSteps it would be nice
    to enable some auto check that specific class attributes have been declared properly

    But this requires that a "check" function is automatically called after initialization.
    Generic python objects don't have this hook, so we can add it with a MetaClass

    I generally tend to avoid meta classes because they are python black magic,
    but this one is pretty simple and gives us the utility we want
    """

    def __call__(cls, *args, **kwargs):
        """Add post-init hook"""
        instance = super().__call__(*args, **kwargs)

        # handle saving all the construction arguments
        init_params = list(inspect.signature(cls.__init__).parameters.values())[1:]
        param_dict = {}
        for i, param in enumerate(init_params):
            if i < len(args):
                param_dict[param.name] = args[i]
            elif param.default is not param.empty:
                param_dict[param.name] = param.default
        param_dict.update(kwargs)

        # run post init function if the class has one
        if post := getattr(cls, "__post_init__", None):
            post(instance)

        # add _init_params private attribute to class
        instance._init_params = param_dict

        return instance


class BaseCurationStep(abc.ABC, metaclass=PostInitMeta):
    """
    The base abstract class for all CurationSteps.

    On a high level, a CurationStep is a callable object that
    wraps/implements some curation function.

    All curation functions can flag molecules with either an 'issue' or a 'note'.
    Issue flags means the chemical 'failed' that curation
    step and should be removed from the final dataset.
    Note flags mean that the curation step has somehow altered the chemical
    (or its representation).
    The curation step will not remove any compounds, just flag them.

    To avoid attaching flags to objects (which allows for easy compatability with RDKit),
    a CurationStep instead calculates a boolean mask to identify which compounds get a flag.
    A operate mask is also calculated for issues.

    If you want to make your own curationStep, see "Defining Curation Steps" in the docs

    Attributes
    ----------
    dependency: set[str], default=set()
        the set of __name__ attributes for the CurationSteps this
        CurationStep is dependent on
    """

    _init_params: dict[str, Any]
    dependency: set[str] = set()
    _description: Optional[str] = None

    @property
    def description(self) -> str:
        """Short description of what the curation function does"""
        return self._description if self._description is not None else "NA"

    def __str__(self) -> str:
        """Return the name of the CurationStep class as a str"""
        return str(self.__class__.__name__)

    def __repr__(self) -> str:
        """Return the str representation of the CurationStep class"""
        return self.__str__()

    def to_json_dict(self):
        """
        Converts the CurationStep to a JSON serializable dictionary

        This is how the curation workflows will save steps

        Returns
        -------
        dict[str, Any]
        """
        return {
            "name": self.__class__.__name__,
            "source_code_hash": hashlib.sha256(
                inspect.getsource(self.__class__).encode("utf-8")
            ).hexdigest(),
            "params": self._init_params,
        }


class Filter(BaseCurationStep, IssueMixin, abc.ABC):
    """
    The base abstract class for all curation steps that filter individual molecules

    Notes
    -----
    This means that the curation function will only every flag molecules with issues.
    It should not update or alter the molecule in anyway.
    If it does, it should be a Update step instead.
    Therefore, the `note` attribute should not be implemented for this class

    Raises
    ------
    CurationStepError
        if the curation function is not defined properly
    """

    def __post_init__(self):
        """Runs after __init__ finishes to check issue and notes are defined properly"""
        if hasattr(self, "note"):
            raise CurationStepError(
                "Filter curation steps should not implement the 'note' attribute"
            )

        if not isinstance(self.issue, str):
            raise CurationStepError(
                f"CurationSteps require that the `issue` "
                f"attribute is a str; "
                f"not a {type(self.issue)}"
            )
        else:
            if self.issue == DEFAULT_ISSUE.format(self.__class__.__name__):
                warnings.warn(
                    f"'issue' description for curation step {self.__class__.__name__} "
                    f"was unset; using default issue description; "
                    f"to stop warning, set the 'issue' attribute "
                    f"to a description of the issue with the molecule",
                    stacklevel=1,
                )

    @abc.abstractmethod
    def _filter(self, mol: Mol) -> bool:
        raise NotImplementedError

    def run_filter(self, molecules: List[Molecule]) -> Tuple[int, int]:
        """
        Runs the Filter curation function

        Will return the number of issues found that occurred

        Parameters
        ----------
        molecules: List[Molecule]
            the molecules to run through the filter step

        Returns
        -------
        (num_updates, num_issues): Tuple[0, int]
            the number of updates and issue that occurred during this step
            filter steps always have 0 updates
        """
        return self.__call__(molecules)

    def __call__(self, molecules: List[Molecule]) -> Tuple[int, int]:
        """Makes Filter curation step callable; calls the `_filter` function"""
        _num_issues = 0
        for molecule in molecules:
            if not molecule.failed_curation:
                if not self._filter(deepcopy(molecule.mol)):
                    molecule.flag_issue(self.get_issue_text())
                    _num_issues += 1
        return 0, _num_issues


class Update(BaseCurationStep, IssueMixin, NoteMixin, abc.ABC):
    """
    The base abstract class for all curation steps that attempt to update/standardize molecules.

    Will tag a note to any chemical that is altered by this step.
    Not all molecules have to change, and notes will only be added
    to the molecules that actually changed

    Unfortunately, RDKit will sometimes alter molecules by updating them in place
    This makes it hard to enable the history tracking of a molecule and recognize if
    a molecule has undergone a change from its original state prior to the update.
    To handle this, a hash of the binary encoding of a molecule is first taken.
    This hash will then be compared to the hash of the returned molecule object.
    This is different than checking if two SMILES are the same for a molecule.
    It accounts for all properties attached to the molecule, including stereochemistry,
    atom ordering, 3D conformers, etc.
    If the hashes are not equal, the note will be attached to the compound.
    If it is, no note will be attached

    This means that the curation function will attempt to alter the molecule in some way.
    If it does not, and is just checking for properties, it should be a Filter step instead.
    Therefore, the `note` attribute must be implemented for this class

    Update curation steps can also have and `issue` attribute. This will get used only if
    the result of `update` is None, which means whatever update was attempted somehow failed
    for a rdkit related reason (like the function timed out or failed to converge).
    In this case, the compound should be flag for removal as it could be missing the update,
    for example if `Add3DConformer` fails to converge, then this molecule will lack a 3D conformer.
    In this case we want to remove it as downstream it is rightfully assumed that
    the molecule has a 3D Conformer, which could cause an un-handled exceptions to be raised.
    """

    def __post_init__(self):
        """Runs after __init__ finishes to check issue and notes are defined properly"""
        if hasattr(self, "issue"):
            if not isinstance(self.issue, str):
                raise CurationStepError(
                    f"CurationSteps require that the `issue` "
                    f"attribute is a str; "
                    f"not a {type(self.issue)}"
                )
            else:
                if self.issue == DEFAULT_ISSUE.format(self.__class__.__name__):
                    warnings.warn(
                        f"'issue' description for curation step {self.__class__.__name__} "
                        f"was unset; using default issue description; "
                        f"to stop warning, set the 'issue' attribute "
                        f"to a description of the issue with the molecule",
                        stacklevel=1,
                    )

        if hasattr(self, "note"):
            if not isinstance(self.note, str):
                raise CurationStepError(
                    f"CurationSteps require that the `note` "
                    f"attribute is a str; "
                    f"not a {type(self.note)}"
                )
            else:
                if self.note == DEFAULT_NOTE.format(self.__class__.__name__):
                    warnings.warn(
                        f"'note' description for curation step {self.__class__.__name__} "
                        f"was unset; using default note description; "
                        f"to stop warning, set the 'note' attribute "
                        f"to a description of the update made to the molecule",
                        stacklevel=1,
                    )

    @abc.abstractmethod
    def _update(self, mol: Mol) -> Optional[Mol]:
        raise NotImplementedError

    def run_update(self, molecules: List[Molecule]) -> Tuple[int, int]:
        """
        Runs the Update curation function

        Will return the number of updates that occurred

        Parameters
        ----------
        molecules: List[Molecule]
            the molecules to run through the update step

        Returns
        -------
        (num_updates, num_issues): Tuple[int, int]
            the number of updates and issue that occurred during this step
        """
        return self.__call__(molecules)

    def __call__(self, molecules: List[Molecule]) -> Tuple[int, int]:
        """Makes CurationStep callable; calls the `_func` function"""
        _update_count = 0
        _issue_count = 0
        for molecule in molecules:
            _updated: bool = False
            if not molecule.failed_curation:
                _new_mol = self._update(deepcopy(molecule.mol))
                if _new_mol is not None:
                    _updated = molecule.update_mol(_new_mol, self.get_note_text())
                else:
                    molecule.flag_issue(self.get_issue_text())
                    _issue_count += 1
            _update_count += _updated
        return _update_count, _issue_count
