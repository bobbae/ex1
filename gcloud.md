## GCloud  
```
cloud components update --version 327.0.0

sysctl -w net.ipv4.ip_forward=1

gcloud projects list



gcloud compute regions list

gcloud compute zones list --filter="region=asia-south1"



gcloud compute machine-types list --zones=asia-south1-a



gcloud compute images list --filter="family=centos-7"


gcloud compute disk-types list --zones=asia-south1-a


gcloud compute instances create my_vm_name \
--zone=asia-south1-a  --machine-type=f1-micro \
--image-project=centos-cloud --image-family=centos-7 \
--boot-disk-type=pd-standard --boot-disk-size=10GB


gcloud compute instances create general-europe-west1 --zone europe-west1-b --machine-type  e2-standard-2 --image-project ubuntu-os-cloud --image-family ubuntu-minimal-2004-lts     --boot-disk-type  pd-standard --boot-disk-size 200GB

gcloud compute instances list

gcloud compute instances describe my_vm_name --zone=asia-south1-a 

gcloud beta compute --project your_project ssh --zone "asia-south1-a" "my_vm_name"
exit


gcloud compute instances create inst-eu-1 --zone=europe-north
1-a --machine-type=f1-micro --image=debian-10-buster-v20200910  --boot-disk-type=pd-standard --boot-disk-size=10GB
--tags=wireguard --image-project debian-cloud


gcloud compute instances create inst-us-1 --zone=us-central1-a --machine-type=n1-standard-4 --image=ubuntu-2004-focal-v20201008  --boot-disk-type=pd-standard --boot-disk-size=200GB --tags=wireguard --image-project ubuntu-os-cloud

gcloud compute instances create inst-eu-1 --zone=europe-north1-a --machine-type=n1-standard-4 --image=ubuntu-2004-focal-v20201008  --boot-disk-type=pd-standard --boot-disk-size=200GB --tags=wireguard --image-project ubuntu-os-cloud

gcloud compute ssh --zone europe-north1-a inst-eu-1
gcloud compute ssh --zone us-central1-a us-1

gcloud compute instances list


gcloud compute instances delete europe-west1-vm --zone europe-west1-b


gcloud compute firewall-rules create wireguard --allow=UDP:51820 --target-tags=wireguard --source-ranges=0.0.0.0/0

gcloud compute instances add-tags my-vm-2    --zone europe-west1-b --tags wireguard

gcloud compute firewall-rules list

gcloud compute firewall-rules describe wireguard-51820


gcloud compute firewall-rules describe wireguard-51820

gcloud compute firewall-rules create wireguard --allow=UDP:51820 --target-tags=wireguard --source-ranges=0.0.0.0/0

gcloud compute instances add-tags my-vm-2    --zone europe-west1-b --tags wireguard

```


