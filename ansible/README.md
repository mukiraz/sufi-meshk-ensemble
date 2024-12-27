# Development Makinenin Ayarlanması.

Sanal Makineyi kurun.

Sanal Makinede ssh hizmetini kurun ve aktif hale getirin.

Sanal makineye giriş yaptıktan sonra şu komutla SSH kurulumunu yapın:

sudo apt update
sudo apt install openssh-server

SSH hizmetini başlatın:

sudo systemctl enable ssh
sudo systemctl start ssh

/etc/ssh/sshd_config dosyasını düzenleyerek yetkilendirme ayarlarını kontrol edin:

    SSH yapılandırma dosyasını açın:

sudo nano /etc/ssh/sshd_config

Şu satırların doğru şekilde ayarlandığından emin olun:

PermitRootLogin yes
PasswordAuthentication yes

Değişiklik yaptıysanız, SSH hizmetini yeniden başlatın:

    sudo systemctl restart ssh

Firewall Ayarlarını Kontrol Edin

Eğer SSH portuna erişim engellenmişse, şu komutla port 22'yi açın:

sudo ufw allow 22
sudo ufw reload


IP adresinizi öğrenin:

ip a

1. SSH Key Pair Oluşturma

Yerel makinenizde aşağıdaki komutu çalıştırarak bir key çifti oluşturabilirsiniz:

ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

Bu komutun detayları:

    -t rsa: RSA algoritması kullanarak bir key çifti oluşturur.
    -b 4096: Key uzunluğunu 4096 bit olarak belirler.
    -C: Key çiftine bir açıklama ekler (genellikle e-posta adresiniz).

2. Key Dosyalarını Kaydetme

Komutu çalıştırdığınızda şu mesajı göreceksiniz:

Enter file in which to save the key (/home/your_user/.ssh/id_rsa):

    Varsayılan konumu kullanmak için Enter tuşuna basabilirsiniz.
    Farklı bir dosya adı istiyorsanız, tam yolunu belirtebilirsiniz (örneğin, /home/your_user/.ssh/my_key).

3. Parola (Passphrase) Ayarlama

Key dosyalarınızı bir parola ile şifrelemek isterseniz, komut şunu soracaktır:

Enter passphrase (empty for no passphrase):

    Parola girin: Daha fazla güvenlik sağlar.
    Boş bırakın: Key dosyasını parolasız kullanabilirsiniz.

4. Public ve Private Key Dosyaları

Bu işlemden sonra aşağıdaki dosyalar oluşturulur:

    Private key (Gizli Anahtar): /home/your_user/.ssh/id_rsa
    Public key (Genel Anahtar): /home/your_user/.ssh/id_rsa.pub

5. Public Key'i Sunucuya Eklemek

Oluşturduğunuz public key'i sanal makinenize eklemek için şu adımları izleyin:

    Public Key'i Kopyalayın: Yerel makineden sanal makineye key'i kopyalayın:

ssh-copy-id -i ~/.ssh/id_rsa.pub username@192.168.1.229

Bu komut, public key'inizi otomatik olarak sanal makinenin ~/.ssh/authorized_keys dosyasına ekler.

Manuel Olarak Eklemek (Alternatif Yöntem):

    Public key'inizi terminalde görüntüleyin:

cat ~/.ssh/id_rsa.pub

Bu key'i kopyalayın ve sanal makinedeki ~/.ssh/authorized_keys dosyasına ekleyin:

    nano ~/.ssh/authorized_keys

    Public key'i yapıştırın ve kaydedin.

Dosya İzinlerini Kontrol Edin: Sanal makinede SSH dosyalarının izinlerini doğru şekilde ayarlayın:

    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_keys

6. SSH ile Public Key Authentication Testi

Şimdi SSH ile parola kullanmadan bağlanmayı deneyin:

ssh username@192.168.1.229

Eğer bağlantı başarılı olursa, key çiftiniz doğru şekilde çalışıyor demektir.

şu komutu yürütün:

ansible-playbook -i ansible/inventories/development/hosts ansible/playbooks/setup.yml --ask-vault-pass

sanal makineniz hazır hale gelecektir.
