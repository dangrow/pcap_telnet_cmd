def process_and_extract_commands_complete(input_path, output_path):
    """
    从原始文件中提取并清理命令。
    
    参数:
        input_path: 原始文件路径
        output_path: 最终清理后的文件路径
    """

    # 第一部分：从原始文件中处理文档内容

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 删除空行和其分隔线
    processed_lines = []
    separator = "-" * 50
    skip_next = False

    for i, line in enumerate(lines):
        if line.strip() == "" and (i + 1) < len(lines) and lines[i + 1].strip() == separator:
            skip_next = True
        elif skip_next and line.strip() == separator:
            skip_next = False
        else:
            processed_lines.append(line)

    # 第二部分：从处理后的文档内容中提取命令

    common_commands = [
        ':', 'add-apt-repository', 'addpart', 'addr2line', 'adduser', 'alias', 'apt', 'apt-add-repository', 'apt-cache', 
        'apt-cdrom', 'apt-config', 'apt-get', 'apt-key', 'apt-mark', 'ar', 'arch', 'as', 'authbind', 'awk', 'b2sum', 
        'base32', 'base64', 'basename', 'bash', 'bashbug', 'bootctl', 'bunzip2', 'busctl', 'busybox', 'bzcat', 'bzcmp', 
        'bzdiff', 'bzegrep', 'bzexe', 'bzfgrep', 'cat', 'chattr', 'chgrp', 'chmod', 'chown', 'chpasswd', 'crontab', 'curl', 
        'cut', 'dd', 'df', 'dir', 'do', 'done', 'du', 'env', 'ethtool', 'export', 'find', 'finger', 'fmt', 'fold', 'free', 
        'fs', 'ftpget', 'gcc', 'grep', 'groupadd', 'groups', 'head', 'ifconfig', 'iptables', 'jobs', 'kill', 'last', 'less', 
        'ln', 'locate', 'ls', 'man', 'mkdir', 'more', 'mount', 'nano', 'nc', 'netstat', 'nice', 'nisdomainname', 'nohup', 
        'passwd', 'perl', 'ping', 'ps', 'python', 'reboot', 'rmdir', 'scp', 'sed', 'service', 'shutdown', 'sleep', 'sort', 
        'ssh', 'su', 'sudo', 'systemctl', 'systemd', 'tail', 'tar', 'tee', 'tftp', 'top', 'touch', 'ulimit', 'umask', 
        'umount', 'uname', 'uniq', 'unset', 'unzip', 'uptime', 'useradd', 'userdel', 'usermod', 'vi', 'vim', 'wc', 'wget', 
        'which', 'yes', 'ypdomainname', 'yum', 'zcat', 'zcmp', 'zdiff', 'zdump', 'zegrep', 'zfgrep', 'zgrep', 'zipdetails', 
        'zipinfo', 'zless', 'zmore', 'znew'
    ]

    extracted_commands = []

    for line in processed_lines:
        line = line.strip()
        
        # 过滤条件
        if line == "#" or line.startswith("Password:") or line.startswith("Login:") or line.isdigit():
            continue
        if line == separator:  # 分隔线
            continue
        
        # 检查 "command not found" 或 "applet not found" 的行
        if "command not found" in line or "applet not found" in line:
            cmd = line.split(":")[0].strip()
            extracted_commands.append(cmd)
        
        # 检查以 ">" 开头的行
        elif line.startswith(">"):
            extracted_commands.append(line[1:].strip())
        
        # 检查以 "/" 或 "./" 开头的行
        elif line.startswith(("/", "./")):
            extracted_commands.extend(line.split(";"))
        
        # 检查以 "rm" 开头的行
        elif line.startswith("rm"):
            extracted_commands.extend(line.split(";"))
        
        # 检查只有一个单词的行
        elif len(line.split()) == 1:
            extracted_commands.append(line)
        
        # 检查以常见命令开头的行
        elif any(line.startswith(cmd) for cmd in common_commands):
            extracted_commands.extend(line.split(";"))

    # 去除空格和空命令
    extracted_commands = [cmd.strip() for cmd in extracted_commands if cmd.strip()]

    # 第三部分：进一步清理提取的命令

    def contains_binary(line):
        """检查行中是否包含二进制字符"""
        return any([char not in set(map(chr, range(32, 127))) and char != '\n' for char in line])
    
    def contains_unwanted_chars(word):
        """检查字符串是否包含不希望出现的字符"""
        return any(char in word for char in ["@", "A", "B", "C", "D", "E", "F", "G", 
                                             "H", "I", "J", "K", "L", "M", "N", "O", 
                                             "P", "Q", "R", "S", "T", "U", "V", "W", 
                                             "X", "Y", "Z", "0", "1", "2", "3", "4", 
                                             "5", "6", "7", "8", "9"])

    # 基于条件过滤行
    filtered_commands = [cmd for cmd in extracted_commands if not (contains_binary(cmd) 
                                                                   or cmd.startswith(" ") 
                                                                   or cmd.startswith("\t") 
                                                                   or cmd.startswith("#") 
                                                                   or cmd.strip() == ""
                                                                   or (len(cmd.split()) == 1 and contains_unwanted_chars(cmd.strip())))]

    # 使用集合去除重复行，但为了保持原始文件中的顺序，我们需要进行一些额外的操作
    seen = set()
    unique_commands = []
    for cmd in filtered_commands:
        if cmd not in seen:
            seen.add(cmd)
            unique_commands.append(cmd)

    # 保存清理后的内容到输出文件
    with open(output_path, "w", encoding="utf-8") as file:
        for cmd in unique_commands:
            file.write(cmd + "\n")


process_and_extract_commands_complete("/root/traffic/telnetdata01.txt", "/root/traffic/cmd21.txt")
