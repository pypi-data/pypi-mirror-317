# SRun SWPU CLI 🖥️

A command-line interface for SWPU (Southwest Petroleum University) network authentication system. This CLI tool provides an easy way to manage your network connection. 🚀

## ✨ Features

- **Simple Commands** 🎯
  - Login to network
  - Logout from network
  - Check connection status

- **Beautiful Output** 🎨
  - Colored status messages
  - Formatted traffic usage
  - Clear error messages

- **Network Support** 🌐
  - China Mobile Wireless
  - China Mobile Wired
  - Student Network
  - Teacher Network
  - China Telecom Wireless

## 📦 Installation & Use

### Install from PyPI

```bash
pip install srun-swpu-cli
```

Or install with user scheme

```bash
pip install --user srun-swpu-cli
```

Or install in virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
pip install srun-swpu-cli
```

### Simply check current connection status
```bash
srun-swpu-cli status
```

### Login Sample
```bash
srun-swpu-cli login \
--student-id student_id \
--network-type china-mobile-wireless \
--password "your_password"
```

### Logout Sample
```bash
srun-swpu-cli logout \
--student-id student_id \
--network-type china-mobile-wireless
``` 
