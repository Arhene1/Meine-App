


    st.subheader("Deine heutigen Aufgaben")
    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            st.write(f"{'✅' if task['done'] else '⬜'} **{task['title']}** · {task['category']}")
    else:
        st.info("Noch keine Aufgaben angelegt. Wähle einen Bereich im Menü und starte mit einem kleinen Schritt.")

    with st.expander("Profil / Begrüßungsname ändern"):
        new_name = st.text_input("Wie soll ich dich nennen?", value=st.session_state.username)
        if st.button("Namen speichern"):
            st.session_state.username = new_name.strip() or "Freundin/Freund"
            st.rerun()

elif page in CATEGORIES:
    category = page
    icon = CATEGORIES[category]
    st.subheader(f"{icon} {category}")
    st.write({
        "Self-Care": "Achte auf dich. Du musst nicht alles auf einmal schaffen.",
        "Wasser": "Eine freundliche Erinnerung: Trinken nicht vergessen.",
        "Essen": "Entdecke einfache Ideen für Mahlzeiten und Snacks.",
        "Fitness": "Bewegung darf klein anfangen und Spaß machen.",
        "Haushalt": "Aus großen Aufgaben werden kleine, machbare Schritte.",
        "Weiteres": "Lege eigene Aufgaben an, die dir wichtig sind.",
    }[category])

    if category == "Wasser":
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.metric("Heute getrunkene Gläser", st.session_state.water_glasses)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💧 Glas hinzufügen", type="primary", use_container_width=True):
                st.session_state.water_glasses += 1
                st.session_state.points += 2
                st.rerun()
        with c2:
            if st.button("Zurücksetzen", use_container_width=True):
                st.session_state.water_glasses = 0
                st.rerun()
        st.caption("Die Anzeige ist ein einfacher Tracker, keine medizinische Trinkmengenempfehlung.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Ideen für kleine Aufgaben")
    for idea in TASK_IDEAS[category]:
        col_a, col_b = st.columns([4, 1])
        with col_a:
            st.write(f"• {idea}")
        with col_b:
            if st.button("＋", key=f"add_{category}_{idea}", help="Aufgabe hinzufügen"):
                st.session_state.tasks.append({"title": idea, "category": category, "done": False})
                st.toast("Aufgabe hinzugefügt!")
                st.rerun()

    st.markdown("#### Eigene Aufgabe")
    custom_task = st.text_input("Was möchtest du erledigen?", key=f"custom_{category}")
    if st.button("Eigene Aufgabe hinzufügen", key=f"custom_btn_{category}"):
        if custom_task.strip():
            st.session_state.tasks.append({"title": custom_task.strip(), "category": category, "done": False})
            st.success("Deine Aufgabe wurde hinzugefügt.")
            st.rerun()

    st.markdown("#### KI-Idee für dich")
    question = st.text_input("Wobei brauchst du eine Idee oder Motivation?", key=f"q_{category}")
    if st.button("KI fragen", key=f"ai_{category}", type="primary"):
        if question.strip():
            with st.spinner("Dein Begleiter überlegt ..."):
                st.session_state[f"answer_{category}"] = ask_ai(question, category)
    if st.session_state.get(f"answer_{category}"):
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.write(st.session_state[f"answer_{category}"])
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "KI-Begleiter":
    st.subheader("💬 Sprich mit deinem KI-Begleiter")
    st.caption("Frag nach Ideen für deinen Alltag, Motivation oder kleinen nächsten Schritten.")
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Was beschäftigt dich gerade?")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Ich denke nach ..."):
                answer = ask_ai(prompt, "Allgemeiner Lifestyle-Begleiter")
            st.markdown(answer)
        st.session_state.chat.append({"role": "assistant", "content": answer})

else:
    st.subheader("⚙️ Einstellungen")
    st.write("Passe deinen Einstieg in Logout an.")
    st.info("Für den ersten Prototyp sind Login und dauerhafte Nutzerkonten noch nicht aktiviert.")
    st.markdown("**KI-Verbindung**")
    if get_api_key():
        st.success("Ein API-Key wurde gefunden.")
    else:
        st.warning("Noch kein API-Key hinterlegt. Die App läuft im Demo-Modus.")
    st.markdown("**Datenschutz**")
    st.write(
        "Diese Demo speichert Aufgaben und Fortschritt nur im Streamlit-Sitzungszustand. "
        "Beim Neustart oder bei einer neuen Sitzung können Daten verloren gehen. "
        "Für eine echte Veröffentlichung sollten Anmeldung, Datenbank, Datenschutztext "
        "und Löschfunktion ergänzt werden."
    )

# Task list and completion controls available on every page
if st.session_state.tasks:
    with st.expander(f"📋 Aufgabenliste ({sum(not t['done'] for t in st.session_state.tasks)} offen)"):
        for i, task in enumerate(st.session_state.tasks):
            c1, c2 = st.columns([5, 1])
            with c1:
                checked = st.checkbox(
                    f"{task['title']} · {task['category']}",
                    value=task["done"],
                    key=f"task_check_{i}",
                )
                if checked and not task["done"]:
                    task["done"] = True
                    st.session_state.points += 10
                    st.toast("Aufgabe geschafft! +10 XP 🎉")
                    st.rerun()
                elif not checked and task["done"]:
                    task["done"] = False
                    st.session_state.points = max(0, st.session_state.points - 10)
                    st.rerun()
