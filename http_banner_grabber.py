import signal
import socket
import sys


# Colors
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def def_handler(sig, frame):
    print(f"{bcolors.FAIL}\n\n[!] Quiting...\n{bcolors.ENDC}")
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


def grab_http_banner(host, port=80):
    """Connects to the specified host and port, sends an HTTP HEAD request,
    and prints the server's response.

    Args:
        host (str): The target host's IP address or domain name.
        port (int): The target port (default is 80).

    Returns:
        None
    """
    try:
        # Create a socket object using IPv4 and TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Setting a timeout to prevent the script from hanging
            s.settimeout(5)

            print(f"Connecting to {host}:{port}...")
            s.connect((host, port))

            # Construct the HTTP HEAD request
            http_request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)

            print("Sending HTTP HEAD request...")
            s.sendall(http_request.encode())

            response = s.recv(1024).decode()

            # Displaying the response
            print(f"\n{bcolors.OKGREEN}[*] Received response:{bcolors.ENDC}\n")
            print(response)

    except socket.timeout:
        print(f"{bcolors.FAIL}Connection timed out.{bcolors.ENDC}")
    except socket.error as e:
        print(f"{bcolors.FAIL}Socket error: {e}{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            f"{bcolors.FAIL}[!]Usage: python http_banner_grabber.py <host>{bcolors.ENDC}"
        )
        sys.exit(1)

    target_host = sys.argv[1]
    grab_http_banner(target_host)
