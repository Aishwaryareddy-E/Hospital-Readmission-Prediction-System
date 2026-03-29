# 🚀 QUICK START GUIDE - Hospital Readmission Project

## ⚡ Complete Setup in 10 Steps

### Step 1: Install Python (if not installed)
Download from: https://www.python.org/downloads/
✅ During installation, CHECK "Add Python to PATH"

### Step 2: Install MySQL
Download from: https://dev.mysql.com/downloads/mysql/
✅ Remember your root password!

### Step 3: Install Project Dependencies
```bash
cd "c:\data science project\hospital-readmission-project"
pip install -r requirements.txt
```

### Step 4: Download Dataset
1. Go to: https://www.kaggle.com/datasets/dubradave/hospital-readmissions
2. Download and extract the CSV file
3. Rename it to `hospital_data.csv`
4. Move to `data/` folder

### Step 5: Set Up Database
1. Open MySQL Workbench
2. Connect to your local MySQL (usually localhost with root password)
3. Open `setup_database.sql` in MySQL Workbench
4. Click the lightning bolt icon (⚡) to run all queries
5. You should see "hospital_db" created

### Step 6: Configure Database Connection
Open `load_data.py` in VS Code
Find this line (around line 27):
```python
engine = create_engine('mysql+mysqlconnector://root:yourpassword@localhost/hospital_db')
```
Replace `yourpassword` with YOUR actual MySQL password

### Step 7: Load Data into Database
In terminal (in project folder):
```bash
python load_data.py
```
✅ You should see: "Total rows loaded: 101,766"

### Step 8: Verify Data
In MySQL Workbench, run:
```sql
USE hospital_db;
SELECT COUNT(*) FROM patients;
```
✅ Should show 101,766 rows

### Step 9: Run Exploratory Data Analysis
```bash
jupyter notebook notebooks/01_eda.ipynb
```
- Click on cells one by one and run them (Shift+Enter)
- Watch the magic happen! ✨
- All plots will be saved to `plots/` folder

### Step 10: Train Your First Model
```bash
python notebooks/03_model_training.py
```
This will:
- Preprocess data
- Train 4 different ML models
- Compare their performance
- Save the best model

⏱ Takes about 2-5 minutes

---

## 🎯 What to Do Next

### Option A: Understand Your Model Better
```bash
python notebooks/04_shap_analysis.py
```
This shows WHY your model makes each prediction

### Option B: Deploy as API
Terminal 1:
```bash
python api/app.py
```

Terminal 2 (new terminal):
```bash
python api/test_api.py
```

Open browser: http://localhost:8000/docs

### Option C: Create Dashboard
1. Open Tableau Public
2. Connect to MySQL database (hospital_db)
3. Drag and drop to create visualizations
4. Build insights dashboard

---

## 📋 Project Checklist

After setup, you should have:

**Folders:**
- [x] data/ (with CSV and processed files)
- [x] notebooks/ (with 4 analysis files)
- [x] api/ (with app.py and test_api.py)
- [x] models/ (will populate after training)
- [x] plots/ (will populate with visualizations)
- [x] report/ (with insights documents)

**Files Created:**
- [x] requirements.txt
- [x] load_data.py
- [x] setup_database.sql
- [x] README.md
- [x] This QUICKSTART.md

**Database:**
- [x] hospital_db created
- [x] patients table created
- [x] 101,766 rows loaded

**Skills You're Learning:**
- [x] Database setup and SQL
- [x] Data loading and cleaning
- [x] Exploratory data analysis
- [x] Machine learning modeling
- [x] Model evaluation
- [x] API deployment
- [x] Business communication

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Error: "Can't connect to MySQL server"
**Windows:**
1. Press Win + R
2. Type `services.msc`
3. Find "MySQL80" service
4. Right-click → Start

### Error: "Access denied for user 'root'@'localhost'"
Edit all Python files and replace password with correct one:
```python
# In load_data.py, 02_preprocessing.py
engine = create_engine('mysql+mysqlconnector://root:YOUR_ACTUAL_PASSWORD@localhost/hospital_db')
```

### Error: "No module named 'imblearn'"
```bash
# Sometimes imbalanced-learn installs differently
pip install imbalanced-learn
```

### Jupyter Notebook Won't Start
```bash
# Try alternative launch method
python -m notebook notebooks/01_eda.ipynb
```

### API Port Already in Use
If port 8000 is busy, edit `api/app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to different port
```

---

## 📞 Getting Help

1. **Check error message carefully** - It usually tells you exactly what's wrong
2. **Google the error** - Someone else has seen it before
3. **Check README.md** - Detailed troubleshooting section
4. **Review notebook comments** - Every step is explained

---

## ⏱️ Estimated Time Investment

| Activity | Time | Frequency |
|----------|------|-----------|
| Initial Setup | 1-2 hours | One-time |
| Data Loading | 15 minutes | One-time |
| EDA | 2-3 hours | Once |
| Model Training | 1 hour | Once |
| SHAP Analysis | 1-2 hours | Once |
| API Deployment | 30 minutes | Once |
| **TOTAL** | **~8 hours** | **Complete in a weekend!** |

---

## 🎓 Learning Path Recommendation

**Day 1:** Setup & Data Loading (Steps 1-8)
- Install everything
- Get data into MySQL
- Run basic SQL queries

**Day 2:** EDA (Step 9)
- Explore the data
- Create visualizations
- Document insights

**Day 3:** Model Training (Step 10)
- Run preprocessing
- Train models
- Compare results

**Day 4:** Model Understanding
- Run SHAP analysis
- Understand predictions
- Document findings

**Day 5:** Deployment
- Set up API
- Test endpoints
- Share with friends!

---

## 💡 Pro Tips

1. **Keep MySQL Workbench open** - You'll query the database often
2. **Save your work frequently** - Especially in Jupyter notebooks
3. **Read the comments** - Every file has detailed explanations
4. **Experiment** - Change parameters and see what happens
5. **Document everything** - Future you will thank present you
6. **Share your progress** - Post on LinkedIn, GitHub, or with friends

---

## ✅ Success Indicators

You're doing great if:

✅ All Python scripts run without errors
✅ MySQL database has 101,766 rows
✅ Plots are being saved to `plots/` folder
✅ Models are training successfully
✅ API returns predictions
✅ You understand what each step does

---

## 🌟 What Makes This Project Special

1. **End-to-End** - Not just modeling, but full deployment
2. **Real Data** - Actual hospital records, not toy datasets
3. **Explainable AI** - Not a black box - you can explain every prediction
4. **Production Ready** - API can be integrated into real systems
5. **Business Impact** - Solves a real healthcare problem
6. **Portfolio Worthy** - Impressive to show employers

---

## 📈 Next Level Challenges

Once you complete the basics:

1. **Hyperparameter Tuning** - Use GridSearchCV to optimize models
2. **Feature Engineering** - Create new features from existing data
3. **Ensemble Methods** - Combine multiple models
4. **Deployment** - Deploy to cloud (AWS/GCP/Azure)
5. **Monitoring** - Track model performance over time
6. **Dashboard** - Build interactive Tableau/Power BI dashboard
7. **Mobile App** - Create React Native app that uses your API

---

**Remember:** Every expert was once a beginner. Take it one step at a time, and you'll build something amazing! 🚀

Good luck! 🍀
