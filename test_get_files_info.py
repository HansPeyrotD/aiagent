from functions.get_files_info import get_files_info


def test():
    # Test with the current directory
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    # Test with the 'pkg' directory
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    # Test with the '/bin' directory
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    # Test with the '../' directory
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)


if __name__ == "__main__":
    test()
