# PyQt Text Utilities (reverse / swapcase)

Petite application desktop en Python + PyQt5 qui montre un menu menant à deux pages :

- "Renverser le texte" : tapez du texte, appuyez sur Submit -> le texte est inversé
- "Inverser maj/min" : tapez du texte, appuyez sur Submit -> majuscules ↔ minuscules

Structure
```
desktop_software_test/
  main.py
  requirements.txt
  ui/
    __init__.py
    main_menu.py
    reverse_text_page.py
    swap_case_page.py
```

Installation
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Usage
- Le menu principal permet de choisir la page.
- Chaque page possède un champ texte, un bouton Submit et un bouton Retour.

Licence: MIT
