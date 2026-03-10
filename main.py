import random
import string
import argparse
from nicknames import NickNamer
import names

# harfler
VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
NUMBERS = "0123456789"

def generate_random_nickname(max_total_chars=12):
    """
    Rastgele, sadece standart harf/rakam içeren, '@' ile başlayan ve
    maksimum belirtilen karakter uzunluğunda bir kullanıcı adı üretir.
    (Varsayılan toplam uzunluk 12 karakterdir)
    """
    # @ var
    max_name_len = max_total_chars - 1
    # 4 karakter ile max_name_len arasında rastgele 
    length = random.randint(4, max_name_len)
    
    # anlamlı?
    generation_type = random.choice(["pronounceable", "random", "with_numbers"])
    
    name = ""
    if generation_type == "pronounceable":
        # harf dizimi
        use_vowel_first = random.choice([True, False])
        for i in range(length):
            if (i % 2 == 0 and use_vowel_first) or (i % 2 != 0 and not use_vowel_first):
                name += random.choice(VOWELS)
            else:
                name += random.choice(CONSONANTS)
                
    elif generation_type == "with_numbers":
        pool = string.ascii_lowercase + NUMBERS
        name += random.choice(string.ascii_lowercase)
        name += "".join(random.choice(pool) for _ in range(length - 1))
        
    else:
        name = "".join(random.choice(string.ascii_lowercase) for _ in range(length))
        
    return f"@{name}"

def generate_meaningful_nickname(max_total_chars=14):
    """
    nicknames ve names paketlerindeki gerçek isim veritabanlarından rastgele
    bir isim seçerek anlamlı bir kullanıcı adı üretir. Sonuna her zaman 3 rakam eklenir.
    """
    nn = NickNamer()
    # nicknames 
    all_names = set()
    lookup = nn.nickname_lookup
    for canonical, nicks in lookup.items():
        all_names.add(canonical)
        all_names.update(nicks)
    
    # names paketinden isim ekle
    for _ in range(200):
        all_names.add(names.get_first_name().lower())
    
    name_list = sorted(all_names)
    max_name_len = max_total_chars - 1  # @ karakteri için
    suffix_len = 3  # her zaman 3 rakam eklenecek
    max_word_len = max_name_len - suffix_len  # isim için kalan alan
    
    # isimleri filtrele -- uzunluk
    fitting_names = [n for n in name_list if len(n) <= max_word_len]
    
    if not fitting_names:
        # Hiç uyan isim yoksa kırp
        name = random.choice(name_list)[:max_word_len]
    else:
        name = random.choice(fitting_names)
    
    # 3 rakam ekle
    suffix = "".join(random.choice("0123456789") for _ in range(suffix_len))
    name += suffix
    
    return f"@{name}"

def generate_name_with_nickname(max_total_chars=14):
    """
    names paketinden isim-soyisim üretir, ardından
    nicknames paketiyle isme uygun bir nickname oluşturur.
    """
    nn = NickNamer()
    first = names.get_first_name()
    last = names.get_last_name()
    
    max_name_len = max_total_chars - 1  # @ karakteri için
    suffix_len = 3
    max_word_len = max_name_len - suffix_len
    
    # isme uygun takma ad ara
    nick_options = nn.nicknames_of(first)
    
    if nick_options:
        # filtre -- uzunluk
        fitting = [n for n in nick_options if len(n) <= max_word_len]
        if fitting:
            base = random.choice(list(fitting))
        else:
            base = random.choice(list(nick_options))[:max_word_len]
    else:
        # takma ad bulunamazsa üret
        base = first.lower()
        strategies = [
            lambda f, l: f[:3] + l[:3],          # ilk 3 + soyisim ilk 3
            lambda f, l: f + l[0],                # isim + soyisim baş harf
            lambda f, l: f[0] + l,                # isim baş harf + soyisim
            lambda f, l: f[:4],                   # ismin ilk 4 harfi
            lambda f, l: f.lower(),               # ismin kendisi
        ]
        strategy = random.choice(strategies)
        base = strategy(first, last).lower()
        if len(base) > max_word_len:
            base = base[:max_word_len]
    
    # 3 rakam ekle
    suffix = "".join(random.choice("0123456789") for _ in range(suffix_len))
    nickname = f"@{base}{suffix}"
    
    return f"{first} {last} ----- {nickname}"

CYAN    = "\033[96m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
MAGENTA = "\033[95m"
DIM     = "\033[2m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

def print_banner(mode="random"):
    banner = f"""{CYAN}{BOLD}
 ███╗   ██╗██╗ ██████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
 ████╗  ██║██║██╔════╝██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
 ██╔██╗ ██║██║██║     █████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
 ██║╚██╗██║██║██║     ██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
 ██║ ╚████║██║╚██████╗██║  ██╗╚██████╔╝███████╗██║ ╚████║
 ╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝{RESET}
{DIM}{'─' * 57}{RESET}"""
    
    mode_labels = {
        "random":  f"  {YELLOW}⚡ Mod: Rastgele Nickname Üretici{RESET}",
        "anlamli": f"  {GREEN}✦ Mod: Anlamlı Nickname Üretici{RESET}",
        "name":    f"  {MAGENTA}👤 Mod: İsim & Nickname Üretici{RESET}",
    }
    
    print(banner)
    print(mode_labels.get(mode, mode_labels["random"]))
    print(f"{DIM}{'─' * 57}{RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Rastgele Kullanıcı Adı (@nickname) Oluşturucu")
    parser.add_argument("-c", "--count", type=int, default=1, help="Üretilecek kullanıcı adı sayısı")
    parser.add_argument("-m", "--max-length", type=int, default=14, help="Toplam maksimum karakter sayısı (@ dahil, varsayılan: 14)")
    parser.add_argument("-v", "--anlamli", action="store_true", help="Anlamlı isimlerden oluşan nickname üretir (nicknames + names paketi kullanılır)")
    parser.add_argument("-n", "--name", action="store_true", help="İsim-soyisim üretip isme uygun nickname oluşturur")
    
    args = parser.parse_args()
    
    if args.name:
        print_banner("name")
        for _ in range(args.count):
            print(f"  {generate_name_with_nickname(max_total_chars=args.max_length)}")
    elif args.anlamli:
        print_banner("anlamli")
        for _ in range(args.count):
            print(f"  {generate_meaningful_nickname(max_total_chars=args.max_length)}")
    else:
        print_banner("random")
        for _ in range(args.count):
            print(f"  {generate_random_nickname(max_total_chars=args.max_length)}")
    
    print(f"\n{DIM}{'─' * 57}{RESET}")

if __name__ == "__main__":
    main()
