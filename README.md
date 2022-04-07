# ids_slow_dos

# Pre-installion Steps

## Windows
### Install Chocolatey
source: https://chocolatey.org/install
First, ensure that you are using an administrative shell - you can also install as a non-admin, check out Non-Administrative Installation.

Install with powershell.exe
NOTE: Please inspect https://community.chocolatey.org/install.ps1 prior to running any of these scripts to ensure safety. We already know it's safe, but you should verify the security and contents of any script from the internet you are not familiar with. All of these scripts download a remote PowerShell script and execute it on your machine. We take security very seriously. Learn more about our security protocols.

With PowerShell, you must ensure Get-ExecutionPolicy is not Restricted. We suggest using Bypass to bypass the policy to get things installed or AllSigned for quite a bit more security.

    Run Get-ExecutionPolicy. If it returns Restricted, then run Set-ExecutionPolicy AllSigned or Set-ExecutionPolicy Bypass -Scope Process.

Now run the following command:
>
Paste the copied text into your shell and press Enter.
Wait a few seconds for the command to complete.
If you don't see any errors, you are ready to use Chocolatey! Type choco or choco -? now, or see Getting Started for usage instructions.
### Install kubectl 
source: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/#install-on-windows-using-chocolatey-or-scoop
Install on Windows using Chocolatey or Scoop

To install kubectl on Windows you can use either Chocolatey package manager or Scoop command-line installer.
    choco
    scoop

choco install kubernetes-cli

Test to ensure the version you installed is up-to-date:

kubectl version --client

Navigate to your home directory:

If you're using cmd.exe, run: cd %USERPROFILE%
cd ~

Create the .kube directory:

mkdir .kube

Change to the .kube directory you just created:

cd .kube

Configure kubectl to use a remote Kubernetes cluster:

New-Item config -type file

### Install base64
choco install base64

### Install Kind
source: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
choco install kind

## Linux
source: 
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.12.0/kind-linux-amd64
chmod +x ./kind
mv ./kind /some-dir-in-your-PATH/kind

### Create predefind kind cluster
Clone repo https://github.com/ThorstenBigT/ids_slow_dos.git
open powershell as admin and naivgate into the repository main folder 
execute following:
kind create cluster --config kind_cluster_config.yaml

### Deploy service with kubectl
open a powershell
#### Go to folder app_deployments
kubectl apply -f namespaces.yaml 
#### Go to folder k8s-dashboard 
install dasboard:
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml
kubectl apply -f dashboard-admin.yaml
wait until dashboard is deployed check with: 
kubectl get pods --all-namespaces
get passsword token: 
kubectl get secret -n kubernetes-dashboard $(kubectl get serviceaccount dashboard-admin-user -n kubernetes-dashboard -o jsonpath="{.secrets[0].name}") -o jsonpath="{.data.token}" | base64 -d
copy token
create proxy:
kubectl proxy
access viar browser:
 http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/ 
 after entering the toke you should see the administraion dashboard
 open new powershell
#### Go to folder app_deployments/rooms/room1 
kubectl apply -f nodered-pcv.yaml
#### Go to folder app_deployments/rooms/
kubectl apply -f room1 
check via dashboard when pods are ready or kubectl
Access nodered via browser: 
localhost:30880
user is admin
password is: password
import flow backup from folder app_deployments/rooms/room1/room1_flow_backup
#### Go to folder app_deployments/rooms/room2 
kubectl apply -f nodered-pcv.yaml
#### Go to folder app_deployments/rooms/
kubectl apply -f room2
check via dashboard when pods are ready or kubectl
Access nodered via browser: 
localhost:30881
user is admin
password is password
import flow backup from folder app_deployments/rooms/room2/room2_flow_backup
#### Go to folder app_deployments/
kubectl apply -f slowdos-attacker
check via dashboard when pods are ready or kubectl
#### Go to folder app_deployments/monitoring-system
kubectl apply -f mosquitto-pvc.yaml
kubectl apply -f neo4j-pvc.yaml
#### Go to folder app_deployments/
kubectl apply -f monitoring-system
check via dashboard when pods are ready or kubectl
access neo4j borwser administration via browser: 
http://localhost:30474/browser/
change connection url to: bolt://localhost:30687
username: neo4j
password: neo4j
set new password to: 1234

## Use applications

## Kind Cheatsheet
source: https://kind.sigs.k8s.io/docs/user/quick-start/#interacting-with-your-cluster
### Create a cluster
kind create cluster # Default cluster context name is `kind`.
...
kind create cluster --name kind-2
### Get clusters
kind get clusters
### Delete cluster
kind delete cluster

