from DockerBuildManagement import BuildManager
import sys

def main():
    """Entry point for the application script"""
    arguments = sys.argv[1:]
    print('Managing solution with arguments: ')
    print(arguments)
    BuildManager.HandleManagement(arguments)

if __name__ == "__main__":
    main()