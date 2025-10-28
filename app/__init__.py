from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


LANGUAGES = {
    "en": "English",
    "ms": "Bahasa Melayu",
}


TRANSLATIONS = {
    "app.title": {
        "en": "Gamified Learning",
        "ms": "Pembelajaran Bermain",
    },
    "nav.home": {"en": "Home", "ms": "Laman Utama"},
    "nav.login": {"en": "Login", "ms": "Log Masuk"},
    "nav.logout": {"en": "Logout", "ms": "Log Keluar"},
    "nav.dashboard": {"en": "Dashboard", "ms": "Papan Pemuka"},
    "nav.quizzes": {"en": "Quizzes", "ms": "Kuiz"},
    "nav.leaderboard": {"en": "Leaderboard", "ms": "Carta Kedudukan"},
    "nav.admin": {"en": "Admin Overview", "ms": "Paparan Admin"},
    "language.switcher_label": {
        "en": "Language",
        "ms": "Bahasa",
    },
    "home.hero_title": {
        "en": "Level Up Your Learning Journey",
        "ms": "Tingkatkan Pengembaraan Pembelajaran Anda",
    },
    "home.hero_subtitle": {
        "en": "Earn XP, unlock badges, and climb the leaderboard while mastering new topics.",
        "ms": "Kumpul XP, buka lencana dan panjat carta sambil menguasai topik baharu.",
    },
    "home.hero_cta": {"en": "View Dashboard", "ms": "Lihat Papan Pemuka"},
    "home.hero_level": {"en": "Level {level}", "ms": "Tahap {level}"},
    "home.hero_streak": {"en": "Streak: {streak}", "ms": "Rentetan: {streak}"},
    "home.hero_badge_points": {"en": "+50 XP bonus", "ms": "+50 XP bonus"},
    "home.features_title": {
        "en": "Why learners love this platform",
        "ms": "Mengapa pelajar menyukai platform ini",
    },
    "home.feature_gamified": {
        "en": "Gamified missions keep motivation high with points, levels, and streaks.",
        "ms": "Misi gamifikasi mengekalkan motivasi dengan mata, tahap dan rentetan.",
    },
    "home.feature_tracking": {
        "en": "Teachers monitor progress in real-time with clear visual analytics.",
        "ms": "Guru memantau kemajuan secara masa nyata dengan analitik visual yang jelas.",
    },
    "home.feature_multilingual": {
        "en": "Switch instantly between English and Malay for inclusive learning.",
        "ms": "Tukar serta-merta antara Bahasa Inggeris dan Melayu untuk pembelajaran inklusif.",
    },
    "home.feature_responsive": {
        "en": "Responsive UI adapts perfectly to mobile, tablet, and desktop.",
        "ms": "UI responsif sesuai untuk mudah alih, tablet dan desktop.",
    },
    "auth.login_title": {"en": "Login", "ms": "Log Masuk"},
    "auth.demo_hint": {
        "en": "Use the credentials shared by your instructor to explore.",
        "ms": "Gunakan kelayakan yang dikongsi pensyarah anda untuk meneroka.",
    },
    "auth.username_label": {"en": "Username", "ms": "Nama Pengguna"},
    "auth.password_label": {"en": "Password", "ms": "Kata Laluan"},
    "auth.login_button": {"en": "Sign In", "ms": "Masuk"},
    "auth.invalid_credentials": {
        "en": "Invalid username or password. Please try again.",
        "ms": "Nama pengguna atau kata laluan tidak sah. Sila cuba lagi.",
    },
    "auth.login_required": {
        "en": "Please log in to continue.",
        "ms": "Sila log masuk untuk meneruskan.",
    },
    "auth.already_logged_in": {
        "en": "You are already signed in.",
        "ms": "Anda sudah log masuk.",
    },
    "dashboard.student_title": {
        "en": "Student Dashboard",
        "ms": "Papan Pemuka Pelajar",
    },
    "dashboard.admin_title": {
        "en": "Administrator Overview",
        "ms": "Paparan Pentadbir",
    },
    "dashboard.overview": {
        "en": "Overview",
        "ms": "Ringkasan",
    },
    "dashboard.xp": {"en": "Experience Points", "ms": "Mata Pengalaman"},
    "dashboard.level": {"en": "Level", "ms": "Tahap"},
    "dashboard.badges": {"en": "Badges", "ms": "Lencana"},
    "dashboard.no_badges": {
        "en": "No badges earned yet. Complete a quiz to unlock your first badge!",
        "ms": "Tiada lencana diperoleh lagi. Selesaikan kuiz untuk membuka lencana pertama anda!",
    },
    "dashboard.recent_progress": {
        "en": "Recent Progress",
        "ms": "Kemajuan Terkini",
    },
    "dashboard.no_progress": {
        "en": "No quiz attempts yet. Start your first challenge!",
        "ms": "Belum ada percubaan kuiz. Mulakan cabaran pertama anda!",
    },
    "dashboard.quiz": {"en": "Quiz", "ms": "Kuiz"},
    "dashboard.score": {"en": "Score", "ms": "Skor"},
    "dashboard.date": {"en": "Completed", "ms": "Selesai"},
    "dashboard.take_quiz": {
        "en": "Take Quiz",
        "ms": "Jawab Kuiz",
    },
    "dashboard.admin_intro": {
        "en": "Monitor learner engagement, completion rates, and XP growth.",
        "ms": "Pantau penglibatan pelajar, kadar penyiapan dan pertumbuhan XP.",
    },
    "dashboard.students": {"en": "Students", "ms": "Pelajar"},
    "dashboard.avg_score": {"en": "Average Score", "ms": "Skor Purata"},
    "dashboard.completed": {"en": "Completed Quizzes", "ms": "Kuiz Selesai"},
    "dashboard.last_active": {"en": "Last Active", "ms": "Terakhir Aktif"},
    "quizzes.title": {"en": "Available Quizzes", "ms": "Kuiz Tersedia"},
    "quizzes.description": {
        "en": "Select a quiz to earn XP and badges.",
        "ms": "Pilih kuiz untuk mengumpul XP dan lencana.",
    },
    "quizzes.points": {"en": "Points", "ms": "Mata"},
    "quizzes.difficulty": {"en": "Difficulty", "ms": "Kesukaran"},
    "quizzes.take_button": {"en": "Start Quiz", "ms": "Mulakan Kuiz"},
    "quizzes.completed_label": {"en": "Completed", "ms": "Selesai"},
    "quiz.submit_button": {"en": "Submit Answers", "ms": "Hantar Jawapan"},
    "quiz.score_feedback": {
        "en": "You scored {score}% and earned {xp} XP!",
        "ms": "Anda mendapat {score}% dan memperoleh {xp} XP!",
    },
    "quiz.updated_feedback": {
        "en": "Your quiz result has been refreshed with the latest score.",
        "ms": "Keputusan kuiz anda telah dikemas kini dengan skor terbaharu.",
    },
    "quiz.not_found": {"en": "Quiz not found.", "ms": "Kuiz tidak ditemui."},
    "leaderboard.title": {
        "en": "Leaderboard",
        "ms": "Carta Kedudukan",
    },
    "leaderboard.description": {
        "en": "Celebrate the top learners in your cohort.",
        "ms": "Raikan pelajar terbaik dalam kumpulan anda.",
    },
    "leaderboard.rank": {"en": "Rank", "ms": "Kedudukan"},
    "leaderboard.student": {"en": "Student", "ms": "Pelajar"},
    "leaderboard.xp": {"en": "XP", "ms": "XP"},
    "leaderboard.level": {"en": "Level", "ms": "Tahap"},
    "leaderboard.badges": {"en": "Badges", "ms": "Lencana"},
    "messages.badge_earned": {
        "en": "New badge unlocked: {badge}!",
        "ms": "Lencana baharu dibuka: {badge}!",
    },
    "messages.quiz_submitted": {
        "en": "Quiz submitted successfully!",
        "ms": "Kuiz berjaya dihantar!",
    },
    "messages.login_success": {
        "en": "Welcome back! You are now signed in.",
        "ms": "Selamat kembali! Anda telah berjaya log masuk.",
    },
    "messages.logged_out": {
        "en": "You have been logged out.",
        "ms": "Anda telah log keluar.",
    },
    "footer.tagline": {
        "en": "Gamified Learning System",
        "ms": "Sistem Pembelajaran Bermain",
    },
}


def translate(key: str, lang: str, **kwargs) -> str:
    values = TRANSLATIONS.get(key)
    if not values:
        text = key
    else:
        text = values.get(lang) or values.get("en") or key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text


def calculate_level(xp: int) -> int:
    return max(1, xp // 250 + 1)


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%d %b %Y, %H:%M")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"

    quizzes = {
        "math-basics": {
            "title": {"en": "Math Basics", "ms": "Asas Matematik"},
            "difficulty": {"en": "Easy", "ms": "Mudah"},
            "points": 120,
            "questions": [
                {
                    "id": "q1",
                    "prompt": {
                        "en": "What is 5 + 7?",
                        "ms": "Berapakah 5 + 7?",
                    },
                    "options": [
                        {"value": "10", "label": {"en": "10", "ms": "10"}},
                        {"value": "11", "label": {"en": "11", "ms": "11"}},
                        {"value": "12", "label": {"en": "12", "ms": "12"}},
                        {"value": "13", "label": {"en": "13", "ms": "13"}},
                    ],
                    "answer": "12",
                },
                {
                    "id": "q2",
                    "prompt": {
                        "en": "Solve 9 × 3.",
                        "ms": "Selesaikan 9 × 3.",
                    },
                    "options": [
                        {"value": "18", "label": {"en": "18", "ms": "18"}},
                        {"value": "27", "label": {"en": "27", "ms": "27"}},
                        {"value": "21", "label": {"en": "21", "ms": "21"}},
                        {"value": "24", "label": {"en": "24", "ms": "24"}},
                    ],
                    "answer": "27",
                },
                {
                    "id": "q3",
                    "prompt": {
                        "en": "What is the square root of 81?",
                        "ms": "Berapakah punca kuasa dua bagi 81?",
                    },
                    "options": [
                        {"value": "9", "label": {"en": "9", "ms": "9"}},
                        {"value": "8", "label": {"en": "8", "ms": "8"}},
                        {"value": "7", "label": {"en": "7", "ms": "7"}},
                        {"value": "6", "label": {"en": "6", "ms": "6"}},
                    ],
                    "answer": "9",
                },
            ],
        },
        "science-fundamentals": {
            "title": {"en": "Science Fundamentals", "ms": "Asas Sains"},
            "difficulty": {"en": "Medium", "ms": "Sederhana"},
            "points": 150,
            "questions": [
                {
                    "id": "q1",
                    "prompt": {
                        "en": "Which planet is known as the Red Planet?",
                        "ms": "Planet manakah dikenali sebagai Planet Merah?",
                    },
                    "options": [
                        {"value": "mars", "label": {"en": "Mars", "ms": "Marikh"}},
                        {"value": "venus", "label": {"en": "Venus", "ms": "Zuhrah"}},
                        {"value": "jupiter", "label": {"en": "Jupiter", "ms": "Musytari"}},
                        {"value": "saturn", "label": {"en": "Saturn", "ms": "Zuhal"}},
                    ],
                    "answer": "mars",
                },
                {
                    "id": "q2",
                    "prompt": {
                        "en": "What gas do plants absorb from the atmosphere?",
                        "ms": "Gas apakah yang diserap tumbuhan daripada atmosfera?",
                    },
                    "options": [
                        {
                            "value": "carbon_dioxide",
                            "label": {
                                "en": "Carbon Dioxide",
                                "ms": "Karbon Dioksida",
                            },
                        },
                        {
                            "value": "oxygen",
                            "label": {"en": "Oxygen", "ms": "Oksigen"},
                        },
                        {
                            "value": "nitrogen",
                            "label": {"en": "Nitrogen", "ms": "Nitrogen"},
                        },
                        {
                            "value": "hydrogen",
                            "label": {"en": "Hydrogen", "ms": "Hidrogen"},
                        },
                    ],
                    "answer": "carbon_dioxide",
                },
                {
                    "id": "q3",
                    "prompt": {
                        "en": "Water freezes at what temperature (°C)?",
                        "ms": "Air membeku pada suhu berapakah (°C)?",
                    },
                    "options": [
                        {"value": "0", "label": {"en": "0°C", "ms": "0°C"}},
                        {"value": "32", "label": {"en": "32°C", "ms": "32°C"}},
                        {"value": "-10", "label": {"en": "-10°C", "ms": "-10°C"}},
                        {"value": "5", "label": {"en": "5°C", "ms": "5°C"}},
                    ],
                    "answer": "0",
                },
            ],
        },
        "history-adventures": {
            "title": {"en": "History Adventures", "ms": "Pengembaraan Sejarah"},
            "difficulty": {"en": "Hard", "ms": "Sukar"},
            "points": 180,
            "questions": [
                {
                    "id": "q1",
                    "prompt": {
                        "en": "In which year did World War II end?",
                        "ms": "Pada tahun berapakah Perang Dunia Kedua tamat?",
                    },
                    "options": [
                        {"value": "1945", "label": {"en": "1945", "ms": "1945"}},
                        {"value": "1939", "label": {"en": "1939", "ms": "1939"}},
                        {"value": "1950", "label": {"en": "1950", "ms": "1950"}},
                        {"value": "1942", "label": {"en": "1942", "ms": "1942"}},
                    ],
                    "answer": "1945",
                },
                {
                    "id": "q2",
                    "prompt": {
                        "en": "Who was the first President of the United States?",
                        "ms": "Siapakah presiden pertama Amerika Syarikat?",
                    },
                    "options": [
                        {
                            "value": "washington",
                            "label": {
                                "en": "George Washington",
                                "ms": "George Washington",
                            },
                        },
                        {
                            "value": "lincoln",
                            "label": {
                                "en": "Abraham Lincoln",
                                "ms": "Abraham Lincoln",
                            },
                        },
                        {
                            "value": "jefferson",
                            "label": {
                                "en": "Thomas Jefferson",
                                "ms": "Thomas Jefferson",
                            },
                        },
                        {
                            "value": "roosevelt",
                            "label": {
                                "en": "Theodore Roosevelt",
                                "ms": "Theodore Roosevelt",
                            },
                        },
                    ],
                    "answer": "washington",
                },
                {
                    "id": "q3",
                    "prompt": {
                        "en": "The Malacca Sultanate reached its peak in which century?",
                        "ms": "Kesultanan Melaka mencapai kemuncaknya pada abad yang mana?",
                    },
                    "options": [
                        {"value": "15", "label": {"en": "15th Century", "ms": "Abad ke-15"}},
                        {"value": "13", "label": {"en": "13th Century", "ms": "Abad ke-13"}},
                        {"value": "16", "label": {"en": "16th Century", "ms": "Abad ke-16"}},
                        {"value": "17", "label": {"en": "17th Century", "ms": "Abad ke-17"}},
                    ],
                    "answer": "15",
                },
            ],
        },
    }

    badges = [
        {
            "id": "first_quiz",
            "name": {"en": "First Step", "ms": "Langkah Pertama"},
            "description": {
                "en": "Complete your first quiz.",
                "ms": "Selesaikan kuiz pertama anda.",
            },
            "condition": lambda user: len(user["progress"]) >= 1,
        },
        {
            "id": "high_scorer",
            "name": {"en": "High Scorer", "ms": "Skor Tinggi"},
            "description": {
                "en": "Achieve at least 90% on any quiz.",
                "ms": "Capai sekurang-kurangnya 90% dalam mana-mana kuiz.",
            },
            "condition": lambda user: any(p["score"] >= 90 for p in user["progress"]),
        },
        {
            "id": "xp_master",
            "name": {"en": "XP Master", "ms": "Pakar XP"},
            "description": {
                "en": "Accumulate 500 XP across quizzes.",
                "ms": "Kumpul 500 XP daripada kuiz.",
            },
            "condition": lambda user: user["xp"] >= 500,
        },
    ]

    users = {
        "admin": {
            "password": "password123",
            "role": "admin",
            "xp": 0,
            "level": 1,
            "badges": [],
            "progress": [],
            "last_active": datetime.utcnow(),
        },
        "amira": {
            "password": "learn123",
            "role": "student",
            "xp": 240,
            "level": calculate_level(240),
            "badges": ["first_quiz"],
            "progress": [
                {
                    "quiz_id": "math-basics",
                    "score": 85,
                    "xp_earned": 102,
                    "completed_at": datetime.utcnow().replace(hour=9, minute=30),
                },
                {
                    "quiz_id": "science-fundamentals",
                    "score": 92,
                    "xp_earned": 138,
                    "completed_at": datetime.utcnow().replace(hour=11, minute=15),
                },
            ],
            "last_active": datetime.utcnow(),
        },
        "benjamin": {
            "password": "quest456",
            "role": "student",
            "xp": 84,
            "level": calculate_level(84),
            "badges": [],
            "progress": [
                {
                    "quiz_id": "math-basics",
                    "score": 70,
                    "xp_earned": 84,
                    "completed_at": datetime.utcnow().replace(hour=14, minute=45),
                }
            ],
            "last_active": datetime.utcnow(),
        },
    }

    def get_language() -> str:
        lang = session.get("language")
        if lang in LANGUAGES:
            return lang
        return "en"

    def current_user():
        username = session.get("username")
        if not username:
            return None
        return users.get(username)

    def get_badge(badge_id: str):
        return next((badge for badge in badges if badge["id"] == badge_id), None)

    def evaluate_badges(user):
        earned = set(user["badges"])
        for badge in badges:
            if badge["id"] in earned:
                continue
            if badge["condition"](user):
                earned.add(badge["id"])
                badge_name = badge["name"].get(g.lang, badge["name"].get("en"))
                flash(
                    translate("messages.badge_earned", g.lang, badge=badge_name),
                    "success",
                )
        user["badges"] = sorted(earned)

    def login_required(role: str | None = None):
        def decorator(view):
            @wraps(view)
            def wrapped(*args, **kwargs):
                user = current_user()
                if not user:
                    flash(translate("auth.login_required", g.lang), "error")
                    return redirect(url_for("login", next=request.path))
                if role and user["role"] != role:
                    abort(403)
                return view(*args, **kwargs)

            return wrapped

        return decorator

    @app.before_request
    def load_language():
        g.lang = get_language()

    @app.context_processor
    def inject_globals():
        now = datetime.utcnow()
        user = current_user()
        return {
            "current_year": now.year,
            "current_user": user,
            "current_language": g.lang,
            "languages": LANGUAGES,
            "t": lambda key, **kwargs: translate(key, g.lang, **kwargs),
            "badge_details": lambda badge_id: get_badge(badge_id),
            "format_datetime": lambda dt: format_datetime(dt)
            if isinstance(dt, datetime)
            else dt,
            "app_title": translate("app.title", g.lang),
        }

    @app.route("/")
    def home():
        user = current_user()
        return render_template("home.html", user=user, quizzes=quizzes)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user():
            flash(translate("auth.already_logged_in", g.lang), "info")
            return redirect(url_for("dashboard"))

        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip().lower()
            password = request.form.get("password", "")
            user = users.get(username)
            if user and user["password"] == password:
                session["username"] = username
                user["last_active"] = datetime.utcnow()
                flash(translate("messages.login_success", g.lang), "success")
                next_url = request.args.get("next")
                return redirect(next_url or url_for("dashboard"))
            error = translate("auth.invalid_credentials", g.lang)
        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        flash(translate("messages.logged_out", g.lang), "info")
        return redirect(url_for("home"))

    @app.route("/language/<lang>")
    def set_language(lang: str):
        if lang in LANGUAGES:
            session["language"] = lang
        return redirect(request.referrer or url_for("home"))

    @app.route("/dashboard")
    @login_required()
    def dashboard():
        user = current_user()
        if user["role"] == "student":
            progress = sorted(
                user["progress"],
                key=lambda item: item["completed_at"],
                reverse=True,
            )
            completed_ids = {p["quiz_id"] for p in progress}
            quiz_cards = []
            for quiz_id, quiz in quizzes.items():
                completed = quiz_id in completed_ids
                summary = {
                    "id": quiz_id,
                    "title": quiz["title"],
                    "points": quiz["points"],
                    "difficulty": quiz["difficulty"],
                    "completed": completed,
                }
                if completed:
                    record = next(p for p in progress if p["quiz_id"] == quiz_id)
                    summary["score"] = record["score"]
                quiz_cards.append(summary)
            badge_map = {badge["id"]: badge for badge in badges}
            return render_template(
                "dashboard.html",
                quiz_cards=quiz_cards,
                progress=progress,
                badge_map=badge_map,
                quizzes=quizzes,
                is_admin=False,
            )

        # Admin view
        student_stats = []
        for username, details in users.items():
            if details["role"] != "student":
                continue
            attempts = details["progress"]
            scores = [record["score"] for record in attempts]
            avg_score = sum(scores) / len(scores) if scores else 0
            student_stats.append(
                {
                    "username": username,
                    "xp": details["xp"],
                    "level": details["level"],
                    "completed": len(attempts),
                    "avg_score": round(avg_score, 1),
                    "last_active": details["last_active"],
                    "badges": details["badges"],
                }
            )
        student_stats.sort(key=lambda item: item["xp"], reverse=True)
        return render_template(
            "dashboard.html",
            is_admin=True,
            student_stats=student_stats,
            quizzes=quizzes,
        )

    @app.route("/quizzes")
    @login_required()
    def quizzes_list():
        user = current_user()
        progress_by_quiz = {record["quiz_id"]: record for record in user["progress"]}
        quiz_summaries = []
        for quiz_id, quiz in quizzes.items():
            progress = progress_by_quiz.get(quiz_id)
            quiz_summaries.append(
                {
                    "id": quiz_id,
                    "title": quiz["title"],
                    "points": quiz["points"],
                    "difficulty": quiz["difficulty"],
                    "completed": progress is not None,
                    "score": progress["score"] if progress else None,
                }
            )
        return render_template("quizzes.html", quizzes=quiz_summaries)

    @app.route("/quiz/<quiz_id>", methods=["GET", "POST"])
    @login_required()
    def quiz_detail(quiz_id: str):
        quiz = quizzes.get(quiz_id)
        if not quiz:
            flash(translate("quiz.not_found", g.lang), "error")
            return redirect(url_for("quizzes_list"))

        user = current_user()
        lang = g.lang

        if request.method == "POST":
            answers = request.form
            total_questions = len(quiz["questions"])
            correct = 0
            for question in quiz["questions"]:
                value = answers.get(question["id"])
                if value and value == question["answer"]:
                    correct += 1

            score_percent = int(round((correct / total_questions) * 100))
            xp_earned = int(round(quiz["points"] * (score_percent / 100)))

            progress_record = next(
                (record for record in user["progress"] if record["quiz_id"] == quiz_id),
                None,
            )

            if progress_record:
                user["xp"] = max(0, user["xp"] - progress_record["xp_earned"])
                progress_record.update(
                    {
                        "score": score_percent,
                        "xp_earned": xp_earned,
                        "completed_at": datetime.utcnow(),
                    }
                )
                flash(translate("quiz.updated_feedback", lang), "info")
            else:
                progress_record = {
                    "quiz_id": quiz_id,
                    "score": score_percent,
                    "xp_earned": xp_earned,
                    "completed_at": datetime.utcnow(),
                }
                user["progress"].append(progress_record)

            user["xp"] += xp_earned
            user["level"] = calculate_level(user["xp"])
            user["last_active"] = datetime.utcnow()
            evaluate_badges(user)

            flash(
                translate(
                    "quiz.score_feedback",
                    lang,
                    score=score_percent,
                    xp=xp_earned,
                ),
                "success",
            )
            return redirect(url_for("dashboard"))

        return render_template("quiz.html", quiz_id=quiz_id, quiz=quiz)

    @app.route("/leaderboard")
    @login_required()
    def leaderboard():
        leaderboard_rows = []
        for username, details in users.items():
            if details["role"] != "student":
                continue
            leaderboard_rows.append(
                {
                    "username": username,
                    "xp": details["xp"],
                    "level": details["level"],
                    "badges": len(details["badges"]),
                }
            )
        leaderboard_rows.sort(key=lambda row: row["xp"], reverse=True)
        return render_template("leaderboard.html", leaderboard_rows=leaderboard_rows)

    return app


app = create_app()
