from app.database import init_db, session, DomainRule

init_db()
s = session()
s.add_all([
    DomainRule(domain="rbc.ru",         element="div", css_class="article__content"),
    DomainRule(domain="vedomosti.ru",   element="div", css_class="b-rubric_news")
])
s.commit()
