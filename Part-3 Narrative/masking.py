def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str]
) -> bool:
    for name in reseller_names:
        if name in text:
            return False
    return True


if __name__ == "__main__":
    # Part 1 top-reseller names
    reseller_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    # Final external-facing narrative
    final_narrative = """
    West region: ALIAS-19 had total spend of INR 75295.09.
    West region: ALIAS-22 had total spend of INR 73882.33.
    South region: ALIAS-12 had total spend of INR 69936.46.
    North region: ALIAS-06 had total spend of INR 64238.97.
    North region: ALIAS-05 had total spend of INR 61825.02.
    """

    # Negative case: raw reseller name must fail
    leaked_narrative = """
    Mumbai Reseller 1 had total spend of INR 75295.09.
    """

    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"

    assert assert_no_raw_names_leak(
        final_narrative,
        reseller_names
    ) is True

    assert assert_no_raw_names_leak(
        leaked_narrative,
        reseller_names
    ) is False

    print("alias_for tests: PASS")
    print("No-raw-name leak test: PASS")
    print("Negative leak test: PASS")