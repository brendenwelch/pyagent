from functions.run_python import run_python_file

def main():
    run_python_file("calculator", "main.py")
    run_python_file("calculator", "tests.py")
    run_python_file("calculator", "../main.py")
    run_python_file("calculator", "nonexistent.py")

main()
