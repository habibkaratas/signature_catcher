import os
import json
import binascii

def find_signature(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        return binascii.hexlify(data).decode('utf-8')

def update_signatures_json(json_path, directory_path, use_custom_lengths):
    existing_signatures = []
    if os.path.exists(json_path):
        with open(json_path, 'r') as json_file:
            existing_signatures = json.load(json_file)

    new_signatures = []

    processed_start_signatures = set()
    processed_file_types = set()

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            start_signature = find_signature(file_path)
            file_type = filename.split('.')[-1].upper()

            if start_signature in processed_start_signatures or file_type in processed_file_types:
                continue
            processed_start_signatures.add(start_signature)
            processed_file_types.add(file_type)

            if use_custom_lengths:
                start_sig_length = int(input(f"Header imza uzunluğu ({file_type}): "))
                end_sig_length = int(input(f"Footer imza uzunluğu ({file_type}): "))
                end_sig_or_length = int(input(f"Alternatif son imza uzunluğu ({file_type}, varsa, yoksa 0): "))
            else:
                start_sig_length = 20  # Default olarak 20
                end_sig_length = 20  # Default olarak 20
                end_sig_or_length = 0

            new_signature = {
                "start_signature": start_signature[:start_sig_length],
                "end_signature": start_signature[-end_sig_length:],
                "end_signature_or": start_signature[-end_sig_or_length:] if end_sig_or_length else "",
                "file_type": file_type
            }

            if not any(sig["file_type"] == file_type and
                       ((sig["end_signature"] == new_signature["end_signature"]) or
                        (sig.get("end_signature_or") and sig["end_signature_or"] == new_signature["end_signature"]))
                       for sig in existing_signatures):
                new_signatures.append(new_signature)

    if new_signatures:
        all_signatures = existing_signatures + new_signatures
        with open(json_path, 'w') as json_file:
            json.dump(all_signatures, json_file, indent=4)

if __name__ == "__main__":
    while True:
        print("1. Imzaları Güncelle")
        print("2. Çıkış")
        
        choice = input("Yapmak istediğin işlemi seç (1/2): ")
        
        if choice == "1":
            json_path = "signatures.json"   # JSON dosyasının yolu
            directory_path = input("Dosyaların bulunduğu klasör: ") #Taranacak Dizin
            use_custom_lengths = input("Imza uzunluklarını belirlemek istiyor musun? (E/H): ").lower() == "e"

            update_signatures_json(json_path, directory_path, use_custom_lengths)
            print("Imzalar güncellendi.")
        elif choice == "2":
            print("Çıkış yapılıyor.")
            break
        else:
            print("Geçersiz seçenek. 1 veya 2 seçin.")
        
        another_operation = input("Başka işlem yapmak istiyor musun? (E/H): ")
        if another_operation.lower() != "e":
            print("Çıkış yapılıyor.")
            break
