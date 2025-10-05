#!/usr/bin/env python3
"""
BotLi Otomatik Güncelleme Scripti
Bu script BotLi'yi GitHub'dan günceller ve gerekirse yeniden başlatır.
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def check_git_repository():
    """Git repository olup olmadığını kontrol eder"""
    try:
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_local_changes():
    """Yerel değişiklik olup olmadığını kontrol eder"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        return result.stdout.strip() != ""
    except:
        return True


def update_botli():
    """BotLi'yi günceller"""
    print("UPDATE: BotLi guncelleme islemi baslatiliyor...")
    
    if not check_git_repository():
        print("ERROR: Bu dizin bir Git repository degil.")
        print("BotLi'yi guncellemek icin once git clone yapin:")
        print("git clone https://github.com/Torom/BotLi.git")
        return False
    
    if check_local_changes():
        print("WARNING: Yerel degisiklikler tespit edildi.")
        print("Guncelleme yapmadan once degisikliklerinizi commit edin veya stash yapin:")
        print("git add . && git commit -m 'Yerel degisiklikler'")
        print("veya")
        print("git stash")
        return False
    
    try:
        # Remote'dan güncellemeleri çek
        print("FETCH: GitHub'dan guncellemeler cekiliyor...")
        fetch_result = subprocess.run(['git', 'fetch', 'origin'], 
                                    capture_output=True, text=True, cwd=os.getcwd())
        
        if fetch_result.returncode != 0:
            print(f"ERROR: Guncellemeler cekilemedi: {fetch_result.stderr}")
            return False
        
        # Yerel ve remote arasındaki farkı kontrol et
        diff_result = subprocess.run(['git', 'rev-list', '--count', 'HEAD..origin/main'], 
                                   capture_output=True, text=True, cwd=os.getcwd())
        
        if diff_result.returncode == 0 and diff_result.stdout.strip():
            commits_behind = int(diff_result.stdout.strip())
            if commits_behind > 0:
                print(f"NEW: {commits_behind} yeni commit bulundu.")
                
                # Güncellemeyi uygula
                print("PULL: Guncelleme uygulaniyor...")
                pull_result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                           capture_output=True, text=True, cwd=os.getcwd())
                
                if pull_result.returncode == 0:
                    print("SUCCESS: BotLi basariyla guncellendi!")
                    
                    # Yeni bağımlılıkları kontrol et
                    if os.path.exists('requirements.txt'):
                        print("PACKAGES: Bagimliliklari kontrol ediliyor...")
                        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                    
                    return True
                else:
                    print(f"ERROR: Guncelleme basarisiz: {pull_result.stderr}")
                    return False
            else:
                print("OK: BotLi zaten guncel.")
        else:
            print("OK: BotLi zaten guncel.")
            
    except Exception as e:
        print(f"ERROR: Guncelleme sirasinda hata: {e}")
        return False
    
    return False


def main():
    """Ana fonksiyon"""
    print("BotLi Otomatik Guncelleme Araci")
    print("=" * 40)
    
    if update_botli():
        print("\nSUCCESS: Guncelleme tamamlandi!")
        print("BotLi'yi yeniden baslatmak icin:")
        print("python user_interface.py")
    else:
        print("\nERROR: Guncelleme yapilamadi.")
        sys.exit(1)


if __name__ == '__main__':
    main()
