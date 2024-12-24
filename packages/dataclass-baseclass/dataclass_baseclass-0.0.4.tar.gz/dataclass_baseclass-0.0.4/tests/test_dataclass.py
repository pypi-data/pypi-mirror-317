# mypy: disable-error-code=call-arg

from pytest import mark, raises

from dataclasses import FrozenInstanceError
from typing import ClassVar, Protocol

from dataclass_baseclass import Data, DataClass

from .conftest import DataClassTestFactory, ToStr


class P(Protocol):
    c_lst: ClassVar[list[str]] = ["Something"]

    s: str

    def gimme_s(self) -> str:
        return self.s


def test_mutable_class_vars() -> None:
    class WithClassVars(DataClass, P):
        c_d: ClassVar[dict[str, str]] = {"s": "Something"}
        c_t: ClassVar[tuple[str, str]] = ("s", "Something")
        c_s: ClassVar[set[str]] = {"Something"}

    wcv = WithClassVars(s="S")  # type: ignore[abstract]
    assert wcv.c_lst == ["Something"]
    assert wcv.c_d == {"s": "Something"}
    assert wcv.c_t == ("s", "Something")
    assert wcv.c_s == {"Something"}
    assert wcv.s == "S"


def test_wrong_params() -> None:
    with raises(
        TypeError,
        match=r"dataclass\(\) got an unexpected keyword argument 'something'",
    ):

        class UnknownArg(
            DataClass, dataclass_params={"something": "whatever"}
        ):
            pass

    with raises(AssertionError, match=r"kw_only"):

        class KWOnly(DataClass, dataclass_params={"kw_only": False}):
            pass


def test_load_interface(dc_test_factory: DataClassTestFactory) -> None:
    _dc, loader = dc_test_factory()

    with raises(
        ValueError,
        match=r"strict mode not supported",
    ):
        loader(strict=True)


@mark.parametrize("frozen", [False, True])
def test_dataclass_base(
    dc_test_factory: DataClassTestFactory,
    test_data: Data,
    str_test_data: ToStr,
    frozen: bool,
) -> None:
    dc, loader = dc_test_factory(frozen, (P,))

    with raises(
        TypeError,
        match=r"C.__init__\(\) missing 1 required keyword-only argument:",
    ):
        e = loader()

    c_data = {**test_data["c"], **{"s": "Something"}}
    e = loader(c=c_data)
    assert e.gimme_s() == "what"
    assert e.d.gimme_s() == e.d.s
    assert e.c.gimme_s() == "Something"

    with raises(
        TypeError,
        match=r"__init__\(\) got an unexpected keyword argument 'unexpected_attr'",
    ):
        dc(i=1, unexpected_attr=True)

    data = str_test_data()
    e = dc(**data)
    assert e.gimme_s() == "what"
    assert type(e.c) is dict


def test_dataclass_mutable(dc_test_factory: DataClassTestFactory) -> None:
    _dc, loader = dc_test_factory(frozen=False)

    e = loader()

    e.i = 12


def test_dataclass_frozen(dc_test_factory: DataClassTestFactory) -> None:
    _dc, loader = dc_test_factory(frozen=True)

    e = loader()

    with raises(FrozenInstanceError, match=r"cannot assign to field"):
        e.i = 12
