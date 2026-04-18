# KINO

Καλησπέρα στο team! Επιτέλους φτιάχτηκε το github! 
Αν δεν έχετε ξανα δουλέψει με git, έγραψα μαζί με το τσατ παπαπατζή λίγες οδηγίες.

Αν είστε βέβαια απο windows μπορείτε απλά να βάλετε το github desktop και να ξεμπερδέψετε...
Οι παρακάτω εντολές ισχύουν από terminal των windows ή linux που είναι λίγο πιο περίεργο.

Παρακάτω είναι οι βασικές οδηγίες για να δουλεύουμε όλοι σωστά χωρίς να μπλέκουμε ο ένας τον άλλον:

Παρακαλώ πολύ στο φάκελο source, να μην έχουν όοολοι ένα script. Ο κάθε ένας να φτιάξει το δικό του.
Το script του logic που λέω εδώ και κάποιες μέρες θα είναι αυτό που θα ενώνει τα επιμέρους .py αρχεία (χρησιμοποιώντας το π.χ. import arxeio.py) για να δημιουργεί το τελικό αποτέλεσμα

🔹 1. Πρώτη φορά (clone το project) 

git clone <repo_link>
cd <project_folder>

(το repo_link είναι το link του github)

🔹 2. Πάντα πριν ξεκινήσεις δουλειά (για να έχεις τις τελευταίες αλλαγές του project)

git checkout main
git pull origin main

🔹 3. Δημιουργία δικού σου branch (ΥΠΟΧΡΕΩΤΙΚΟ)
Ο καθένας δουλεύει ΜΟΝΟ στο δικό του branch.

Format:

git checkout -b gui/τι-κάνεις (π.χ. ένα branch μπορεί να λέγεται GUI/starting. το επόμενο μπορεί να λέγεται GUI/arxiko_layout κτλ κτλ)
git checkout -b logic/τι-κάνεις (για ό,τι έχει να κάνει με logic)
git checkout -b db/τι-κάνεις (για ό,τι έχει να κάνει με database)

π.χ.:

gui/arxiko-layout, gui/dimiourgia-arithmwn-se-grid
logic/enwsi-logic-me-gui, logic/random-number-generatio
db/arxiko-layout, db/testing-erwtimata

🔹 4. Κάνεις αλλαγές + commit

git add .
git commit -m "Τι άλλαξα" (π.χ. "Έφτιαξα το αρχικό layout του ΚΙΝΟ)

🔹 5. Push το branch σου

git push origin <το όνομα του branch σου>
π.χ. git push origin gui/arxiko-layout

🔹 6. Όταν θέλεις να πάρεις updates από main
(ΣΗΜΑΝΤΙΚΟ για να μην υπάρχουν conflicts)

git checkout main
git pull origin main
git checkout το-branch-sou
git merge main

🔹 7. Όταν τελειώσεις αυτό που κάνει στο branch σου
Κάνεις Pull Request στο GitHub (από το branch σου → main)

Μετά μπορείς να δημιουργήσεις καινούριο branch κανονικά

ΔΕΝ κάνουμε ποτέ push κατευθείαν στο main.

🔹 Κανόνες ομάδας

❌ Δεν δουλεύουμε στο main
❌ Δεν κάνουμε push στο main
✅ Πάντα branch
✅ Συχνά pull για updates
✅ Καθαρά commit messages

🔹 Δομή project (για να μη μπλεκόμαστε)

GUI → ένας υπεύθυνος
Logic → ένας υπεύθυνος
Database → ένας υπεύθυνος

Αν κάποιος χρειαστεί να πειράξει κάτι αλλού που προφανώς θα χρειαστεί, παρακαλώ πολύ πρώτα συνεννόηση.

Αν κάτι δεν δουλεύει ή κολλήσετε, γράψτε discord εννοείται.