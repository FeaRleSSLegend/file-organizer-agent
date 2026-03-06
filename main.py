from organizer import run_agent

def main():
    try:
        path = input("Enter the path: ")
        instruction = input("What would you like me to do: ")

        run_agent(path, instruction)

    except Exception as e:
        return f"Error: {e}"
if __name__ == "__main__":
    main()
