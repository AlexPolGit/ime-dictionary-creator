from pathlib import Path

from ime_dictionary_creator.microsoft_ime import MicrosoftImeDictionary

if __name__ == "__main__":
    dict = MicrosoftImeDictionary(name="test")
    dict.add_entry("ことば", "言葉")
    dict.add_entry("ごれい", "語例")
    dict.add_comment("何か")
    dict.add_entry("さとう", "佐藤さん", "人名")
    dict.save_to_file()

    dict2 = MicrosoftImeDictionary.from_file(Path("test.txt"), "test2")
    dict2.add_entry("はんたーはんたー", "HUNTER×HUNTER")
    dict2.save_to_file()
