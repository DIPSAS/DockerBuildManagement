from DockerBuildManagement import BuildManager
import sys

def main():
    """Entry point for the application script"""
    arguments = sys.argv[1:]
    BuildManager.HandleManagement(arguments)

if __name__ == "__main__":
    main()