import subprocess

# Verify that the script is being executed
print("Starting SSL renewal script")


filename = "/etc/apache2/conf/httpd.conf" # Replace with the actual file name
search_string = "Include \"/etc/apache2/conf.d/userdata/std/2_4/sanjai/sanjai.redux.cloud/" # Replace with the string to search for

with open(filename, "r+") as f:
    lines = f.readlines()
    f.seek(0)
    for line in lines:
        if search_string in line:
            if not line.startswith("#"):
                line = "#" + line
                print("Modified line: ", line.strip()) # Print the modified line
            else:
                print("Already commented line: ", line.strip()) # Print the already commented line
        f.write(line)
    f.truncate()

if subprocess.call(["httpd", "-t", "-f", "/etc/apache2/conf/httpd.conf"]) != 0:
    print("There was an error in the syntax of the Apache configuration file")
else:
    subprocess.call(["systemctl", "restart", "httpd.service"])
    print("The Apache web server was restarted successfully")

# Renew SSL certificates using cPanel's certbot for a specific user
result = subprocess.run(["/usr/local/cpanel/3rdparty/bin/certbot", "renew", "--user", "sanjai"], capture_output=True)
if result.returncode != 0:
    print("Error renewing SSL certificate: ", result.stderr)    
