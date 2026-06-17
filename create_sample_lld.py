"""Create a sample LLD xlsx file from the provided OS course data for testing."""
import pandas as pd

data = [
    {
        "Module Name": "Linux Foundations & Command Line Mastery",
        "LU sequence": 1.8,
        "LU Name": "Shell Scripting Fundamentals",
        "Slugs": "linux_administration_5_v1_lu9",
        "Learning Path": "Bonus",
        "Learning Objectives": "Understand how shell scripts automate repetitive tasks and simplify Linux system administration.",
        "Learning Outcomes": "You will be able to write and execute basic shell scripts to automate routine operations.",
        "Bridge from Previous LU": "",
        "Bridge to Next LU": "",
        "Session Flow (45 mins)": """0–5 min    Motivation hook. Mentor shows a terminal: "I need to create home directories for 20 new interns." Types the commands once, then asks: "Want to do this 20 times?" → introduces the idea of a script
5–12 min    Variables and echo. name="Riya", echo "Hello $name". Difference between single quotes (literal) and double quotes (expanded). read for user input. Command substitution: today=$(date)
12–22 min    Conditionals. if [ -f /etc/passwd ]; then ... fi. Test operators: -f, -d, -z, -eq, -gt. Students write: check if a file exists, print message either way
22–32 min    For loop. for user in alice bob charlie; do mkdir /home/$user; done. Students write: loop over 5 names, create a directory for each, echo confirmation
32–42 min    Combine it. Students write a single script that: (a) accepts a username as argument $1, (b) checks if a home directory already exists, (c) creates it if not, (d) prints a message. Run it 3 times with different usernames
42–45 min    Wrap-up. chmod +x, ./script.sh vs bash script.sh. Where to save scripts (~/bin/, /usr/local/bin/). Mention: this is how real admin automation starts""",
        "FA Type": "Assignment",
        "Assessment Details": """What students submit: Screenshot showing:
The script file open in nano/vim (or cat script.sh output) — code must be visible
Terminal output of the script running with at least 2 different inputs
The created directories visible via ls or ls -la
Passing bar: Script must use at least one variable, one conditional, and produce visible output. Directory creation must succeed.""",
        "References & Resources": "NA",
        "HLD mapping": "CO1",
        "Level of effort": "full",
        "Note for authors": """Keep scripting syntax minimal — this is a first exposure. No functions, no arrays, no $? error handling yet.
The worked example (home directory creation) mirrors what M2 does with user management — a deliberate cross-LU bridge.
The misconception to address: "Scripts are just commands pasted into a file." Show the value of variables and logic that raw command-line can't do.
Avoid bash version-specific gotchas — stick to POSIX-compatible constructs.""",
        "Completeion status": "Pending"
    },
    {
        "Module Name": "User & Permission Management",
        "LU sequence": 2.12,
        "LU Name": "Extended ACLs with setfacl / getfacl",
        "Slugs": "linux_administration_5_v1_lu21",
        "Learning Path": "Bonus",
        "Learning Objectives": "Learn how Access Control Lists provide fine-grained permission management beyond standard Linux permissions.",
        "Learning Outcomes": "You will be able to configure and inspect ACLs using setfacl and getfacl commands.",
        "Bridge from Previous LU": "",
        "Bridge to Next LU": "",
        "Session Flow (45 mins)": """0–10 min    The gap standard permissions can't fill. Scenario: /shared/reports/ is owned by alice (group finance). Bob (group engineering) needs read access to one specific subdirectory, but not the whole tree. With standard permissions, you'd have to change ownership or group — both are wrong. ACLs solve this. Show the + symbol in ls -l output: drwxrwxr-x+
10–20 min    setfacl. setfacl -m u:bob:r-- /shared/reports/q3/. Syntax breakdown: -m (modify), u: (user), g: (group), o: (other). Multiple entries in one command. setfacl -x to remove. setfacl -b to remove all ACLs
20–30 min    getfacl. Read the output — user::rwx, user:bob:r--, group::r-x, mask::rwx, other::r-x. Explain the mask (effective permission ceiling). Verify bob's access by switching user and testing
30–42 min    Hands-on scenario. Setup: 3 users (alice, bob, carol) and 3 directories. Students must: (a) give bob read-only on dir1, (b) give carol read+execute on dir2, (c) give a group devteam write on dir3, (d) verify each with getfacl and by actually accessing as each user
42–45 min    Wrap-up. When to use ACLs vs changing group ownership. Real use case: shared project directories in a company""",
        "FA Type": "Assignment",
        "Assessment Details": """What students submit: Screenshot showing:
getfacl output for all 3 directories with ACLs applied
Terminal output showing at least one user successfully accessing (or being denied access to) a directory based on ACL
Passing bar: ACL entries must be correctly set. getfacl output must show the specific user/group entries, not just standard permissions.""",
        "References & Resources": "NA",
        "HLD mapping": "CO2",
        "Level of effort": "full",
        "Note for authors": """The mask line in getfacl confuses students — spend 2 minutes on it explicitly. A mask of r-- caps bob's effective permission even if the ACL says rwx.
This LU directly bridges to the M2 Project (Building a Secure System) — students will use ACLs in the project.
Cross-course bridge: ACL concepts appear in DevOps Foundations when setting up shared CI/CD artifact directories.""",
        "Completeion status": "Pending"
    },
    {
        "Module Name": "File Systems & Process Management",
        "LU sequence": 3.12,
        "LU Name": "Archiving and Compression",
        "Slugs": "linux_administration_5_v1_lu34",
        "Learning Path": "Bonus",
        "Learning Objectives": "Understand techniques for combining, compressing, and managing files for storage and transfer.",
        "Learning Outcomes": "You will be able to create, extract, and manage compressed archives using Linux tools.",
        "Bridge from Previous LU": "",
        "Bridge to Next LU": "",
        "Session Flow (45 mins)": """0–8 min    Archiving vs compression — the confusion. Many students think "zip = archive + compress together." Linux separates them. tar = packs files into one. gzip/bzip2/xz = shrinks the size. You can combine them or use them separately. Analogy: packing a suitcase (tar) vs vacuum-compressing the bag (gzip)
8–20 min    tar fundamentals. Flags that matter: c (create), x (extract), t (list contents), v (verbose), f (filename). Always f last. Create: tar -cvf archive.tar /etc/. List: tar -tvf archive.tar. Extract: tar -xvf archive.tar -C /restore/. Common mistake: running as root when not needed
20–32 min    Adding compression. tar -czvf archive.tar.gz /etc/ — the z flag pipes through gzip. tar -cjvf archive.tar.bz2 /etc/ — j for bzip2. tar -cJvf archive.tar.xz /etc/ — J for xz. Show size comparison: .tar vs .tar.gz vs .tar.bz2 vs .tar.xz. Speed vs size tradeoff.
32–42 min    Hands-on: full backup workflow. Students: (a) create a directory ~/project/ with 5 files of different types, (b) archive + gzip it to /tmp/project-backup.tar.gz, (c) list contents without extracting, (d) extract to a new location ~/restored/, (e) verify contents match
42–45 min    Quick mention: zip. zip -r archive.zip directory/ and unzip archive.zip. When to use it: sharing with Windows users. Not the Linux-native way but useful to know""",
        "FA Type": "Assignment",
        "Assessment Details": """What students submit: Screenshot showing:
tar -tvf project-backup.tar.gz output — all files listed inside the archive
Extracted directory ~/restored/ with ls -la showing contents match original
du -sh size comparison between original directory and compressed archive""",
        "References & Resources": "NA",
        "HLD mapping": "CO 3",
        "Level of effort": "full",
        "Note for authors": """This LU is the silent pre-requisite for M5's backup LU (5.7/5.8 use tar and rsync). Students who skipped this would struggle there. Make that bridge explicit in the content.
The most common mistake: forgetting -C in extract and dumping files in the current directory. Build this into the error-handling section.
Keep it to gzip and bzip2 in depth. Mention xz for completeness. Skip 7z, rar — not standard Linux admin tools.""",
        "Completeion status": "Pending"
    },
    {
        "Module Name": "Network Configuration & Services",
        "LU sequence": 4.11,
        "LU Name": "SSL/TLS Certificate Management",
        "Slugs": "linux_administration_5_v1_lu47",
        "Learning Path": "Bonus",
        "Learning Objectives": "Understand the role of SSL/TLS certificates in securing communication and managing trust.",
        "Learning Outcomes": "You will be able to generate, inspect, and manage SSL/TLS certificates for secure systems.",
        "Bridge from Previous LU": "",
        "Bridge to Next LU": "",
        "Session Flow (45 mins)": """0–10 min    Why HTTP is broken. Packet sniffing analogy: sending a postcard (HTTP) vs a sealed letter (HTTPS). What an attacker on the same network can see with HTTP — credentials, session cookies, form data. Real incident: the 2014 Firesheep tool that let anyone at a coffee shop hijack Facebook sessions over HTTP. Establish stakes before diving into solution
10–22 min    The PKI model. Three actors: (1) the website (has a private key), (2) the CA (Certificate Authority — e.g., Let's Encrypt, DigiCert), (3) the browser (has a pre-installed list of trusted CAs). Certificate = a document that says "this public key belongs to kalvium.com, and DigiCert vouches for it." Browser checks: Is the CA in my trust list? Is the domain in the cert matching what I connected to? Is the cert expired? Chain of trust: Root CA → Intermediate CA → End-entity cert
22–32 min    The HTTPS handshake (simplified). Browser says hello + lists cipher suites it supports. Server sends its certificate + selected cipher. Browser validates cert against CA trust list. Both derive a session key (without sending it over the wire — Diffie-Hellman magic, no need to explain the math). All further communication encrypted with session key
32–42 min    The certbot workflow. What certbot does: proves domain ownership (HTTP-01 challenge), gets cert from Let's Encrypt, installs it into Apache/Nginx config, sets up auto-renewal. Key files: fullchain.pem, privkey.pem. Core commands: certbot --apache, certbot renew, certbot certificates
42–45 min    Wrap-up. The project (M4-13) will ask students to configure HTTPS on their web server.""",
        "FA Type": "Quiz",
        "Assessment Details": "Quiz",
        "References & Resources": "NA",
        "HLD mapping": "CO4",
        "Level of effort": "full",
        "Note for authors": """This is the most concept-dense of the 5 new LUs. Resist the urge to go into cryptographic detail — that's a full crypto course. The goal is: students can configure HTTPS and understand what they're doing and why it matters.
The Firesheep incident (2010) is well-documented and perfect for this — real tool, real impact, real reason HTTPS adoption accelerated.
CLU format is intentional: VM lab constraints (certbot requires a public domain for HTTP-01 challenge) make a 45-min practical session impossible for most students.
Cross-course bridge: Backend Web Development course (TC_00029) will reference HTTPS setup.""",
        "Completeion status": "Pending"
    },
    {
        "Module Name": "Security & System Troubleshooting",
        "LU sequence": 5.11,
        "LU Name": "Rescue Mode & Boot Recovery",
        "Slugs": "linux_administration_5_v1_lu60",
        "Learning Path": "Bonus",
        "Learning Objectives": "Learn how Linux recovery mechanisms help troubleshoot and restore unbootable systems.",
        "Learning Outcomes": "You will be able to access rescue environments and perform basic boot recovery operations.",
        "Bridge from Previous LU": "",
        "Bridge to Next LU": "",
        "Session Flow (45 mins)": """0–5 min    War story framing. "2am call. Production server is unreachable. You reboot it remotely. It doesn't come back. SSH times out." What do you do? This session gives you the answer. A misconfigured /etc/fstab is the #1 reason for this exact scenario
5–15 min    The boot sequence. Visual diagram walked step by step: (1) BIOS/UEFI, (2) GRUB, (3) Kernel, (4) initrd/initramfs, (5) systemd — PID 1
15–20 min    rescue.target vs emergency.target. rescue.target = systemd managed to mount root read-write, basic services running. emergency.target = minimal shell, root may be read-only
20–22 min    Snapshot — non-negotiable. Before touching anything: open VirtualBox → take snapshot → name it before-rescue-lab
22–27 min    Introduce the corruption. Students add fake UUID line to /etc/fstab. Save file. sudo reboot. VM fails to boot, drops to emergency shell
27–42 min    Recovery — step by step. (1) journalctl -xb | grep -i "failed|error", (2) mount -o remount,rw /, (3) nano /etc/fstab — comment out fake line, (4) systemctl reboot
42–45 min    Wrap-up. mount -a as pre-reboot fstab validation. The habit to build.""",
        "FA Type": "Assignment",
        "Assessment Details": """What students submit — 3 screenshots:
The emergency mode shell prompt showing the systemd error message (before recovery)
The /etc/fstab file with the fake UUID line commented out (after editing, before reboot)
Successful normal boot — either the login prompt or systemctl status showing normal multi-user.target""",
        "References & Resources": "NA",
        "HLD mapping": "CO5",
        "Level of effort": "full",
        "Note for authors": """The snapshot step is pedagogically important — frame it as "sysadmin habit" not "classroom safety net."
The fake UUID aaaabbbb-cccc-dddd-eeee-ffffaaaabbbb is deliberately obvious so students can spot it in fstab immediately.
Mentor script must include: what the emergency shell prompt looks like, the exact error message to expect in journalctl, and the "filesystem is read-only" error when students skip the remount step.
mount -a as a pre-reboot fstab validation command belongs in the wrap-up as the key takeaway habit.
Cross-LU bridge: M3-05 (Permanent Disk Connections) is where students first write fstab entries.""",
        "Completeion status": "Pending"
    }
]

df = pd.DataFrame(data)
df.to_excel("data/sample_os_lld.xlsx", index=False, engine="openpyxl")
print(f"✅ Created sample LLD with {len(df)} LUs → data/sample_os_lld.xlsx")
print(f"   Modules: {df['Module Name'].unique().tolist()}")
