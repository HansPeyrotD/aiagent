from functions.write_file import write_file

def test():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    result = write_file("calculator", "pkg/test.txt", "This is another test file.")
    print(result)

    result = write_file("calculator","/bin/test.txt", "This should fail.")
    print(result)

if __name__ == "__main__":    
    test()