import sys
import os

print("--- STEP 1: Script Started ---")
print(f"Current Working Directory: {os.getcwd()}")

try:
    print("--- STEP 2: Importing uralicNLP ---")
    from uralicNLP import uralicApi # pip install uralicNLP
    print("Success: uralicNLP imported.")
except ImportError as e:
    print(f"ERROR: Could not import uralicNLP. Did you run 'pip install uralicNLP'?\nDetails: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: An unexpected error occurred during import.\nDetails: {e}")
    sys.exit(1)

# 基本単語リスト
base_words = [{"fi": "koti", "en": "home"}]

# 生成する格
cases_to_generate = [{"morph": "+N+Sg+Gen", "suffix_en": "'s"}]

final_list = []

try:
    print("--- STEP 3: Checking/Downloading Model ---")
    # 既にインストールされているか確認
    if not uralicApi.is_language_installed("fin"):
        print("Model 'fin' not found. Downloading... (This might take time)")
        uralicApi.download("fin")
        print("Download complete.")
    else:
        print("Model 'fin' is already installed.")

    print("--- STEP 4: Generating Words ---")
    for word in base_words:
        query = word["fi"] + cases_to_generate[0]["morph"]
        print(f"Trying to generate: {query}")
        
        # ここが最重要ポイント
        generated = uralicApi.generate(query, "fin")
        print(f"Raw result from API: {generated}")
        
        if generated:
            final_list.append(generated[0][0])

    print(f"--- STEP 5: Saving File ---")
    filename = "finnish_debug_output.json"
    import json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_list, f)
    
    print(f"SUCCESS! File saved to: {os.path.abspath(filename)}")

except Exception as e:
    print(f"ERROR during execution: {e}")