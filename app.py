from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import os
import socket

# ---------------- КОНФИГУРАЦИЯ ---------------- #

PORT = int(os.getenv("PORT", "8000"))


class SimpleHandler(BaseHTTPRequestHandler):

    def _serve_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_error(self, code, message=None):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(f"Error {code}: {message}".encode("utf-8"))

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        path = self.path.rstrip("/") or "/"

        # ---------------- СТИЛИ (NEO-BRUTALISM) ---------------- #

        base_styles = """
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Courier New', monospace;
    background: #fafafa;
    color: #000;
    line-height: 1.6;
  }
  nav {
    background: #FFE500;
    border-bottom: 6px solid #000;
    padding: 0;
    position: sticky;
    top: 0;
    z-index: 999;
  }
  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
  }
  .logo {
    font-weight: 900;
    font-size: 1.8rem;
    color: #000;
    text-decoration: none;
    text-transform: uppercase;
  }
  .nav-links {
    display: flex;
    gap: 1.5rem;
  }
  .nav-links a {
    color: #000;
    text-decoration: none;
    font-weight: 700;
    padding: 0.5rem 1rem;
    border: 3px solid transparent;
    transition: all 0.2s;
  }
  .nav-links a:hover, .nav-links a.active {
    border: 3px solid #000;
    background: #fff;
  }
  .mobile-nav {
    display: none;
  }
  @media (max-width: 768px) {
    .nav-links { display: none; }
    .mobile-nav {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    .mobile-nav a {
      color: #000;
      text-decoration: none;
      font-weight: 700;
      padding: 0.75rem;
      border: 3px solid #000;
      background: #fff;
      text-align: center;
    }
  }
  .hero {
    background: #FF6B35;
    border-bottom: 6px solid #000;
    padding: 4rem 2rem;
    text-align: center;
  }
  .hero h1 {
    font-size: 3rem;
    font-weight: 900;
    text-transform: uppercase;
    color: #000;
    margin-bottom: 1rem;
    text-shadow: 4px 4px 0 #fff;
  }
  .hero p {
    font-size: 1.3rem;
    color: #fff;
    font-weight: 700;
  }
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 2rem;
  }
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }
  .card {
    background: #fff;
    border: 5px solid #000;
    padding: 2rem;
    box-shadow: 8px 8px 0 #000;
    transition: all 0.3s;
  }
  .card:hover {
    box-shadow: 12px 12px 0 #000;
    transform: translate(-4px, -4px);
  }
  .card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #000;
    font-weight: 900;
    text-transform: uppercase;
  }
  .card p {
    font-size: 1rem;
    color: #333;
  }
  .section {
    margin-bottom: 3rem;
  }
  .section h2 {
    font-size: 2.5rem;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    color: #000;
  }
  .pricing {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }
  .price-card {
    background: #00D9FF;
    border: 5px solid #000;
    padding: 2rem;
    text-align: center;
    box-shadow: 8px 8px 0 #000;
  }
  .price-card h3 {
    font-size: 2rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
  }
  .price-card .price {
    font-size: 3rem;
    font-weight: 900;
    color: #000;
    margin: 1rem 0;
  }
  .price-card ul {
    list-style: none;
    text-align: left;
    margin: 1rem 0;
  }
  .price-card ul li {
    padding: 0.5rem 0;
    border-bottom: 2px solid #000;
    font-weight: 700;
  }
  .price-card ul li:last-child {
    border-bottom: none;
  }
  .btn {
    display: inline-block;
    background: #FFE500;
    color: #000;
    padding: 1rem 2rem;
    border: 4px solid #000;
    font-weight: 900;
    text-decoration: none;
    text-transform: uppercase;
    box-shadow: 6px 6px 0 #000;
    transition: all 0.2s;
  }
  .btn:hover {
    box-shadow: 8px 8px 0 #000;
    transform: translate(-2px, -2px);
  }
  footer {
    background: #000;
    color: #FFE500;
    text-align: center;
    padding: 2rem;
    border-top: 6px solid #FFE500;
    font-weight: 700;
  }
</style>
"""

        def get_nav(active_path):
            links = [
                ("/", "ГЛАВНАЯ"),
                ("/bots", "УСЛУГИ"),
                ("/hosting", "ХОСТИНГ"),
                ("https://t.me/krimexAI", "TELEGRAM"),
            ]
            desk_html = ""
            mob_html = ""
            for href, label in links:
                cls = "active" if href == active_path else ""
                desk_html += f'<a href="{href}" class="{cls}">{label}</a>'
                mob_html += f'<a href="{href}" class="{cls}">{label}</a>'
            return f"""
<nav>
  <div class="nav-container">
    <a href="/" class="logo">KRIMEX</a>
    <div class="nav-links">
      {desk_html}
    </div>
  </div>
  <div class="mobile-nav container">
    {mob_html}
  </div>
</nav>
"""

        # ---------------- ГЛАВНАЯ ---------------- #

        if path == "/":
            html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KRIMEX | Разработка Telegram ботов</title>
  {base_styles}
</head>
<body>
{get_nav("/")}

<div class="hero">
  <h1>KRIMEX DEVELOPMENT</h1>
  <p>Разработка Telegram/Discord ботов, и инфраструктура. Без лишних слов, только рабочий код.</p>
</div>

<div class="container">
  <div class="section">
    <h2>МОИ ПРОЕКТЫ</h2>
    <div class="cards">
      <div class="card">
        <h3>🤖 KRIMEXAI</h3>
        <p>Мощный ассистент в Telegram. Пишет код, решает задачи, генерирует контент.</p>
      </div>
      <div class="card">
        <h3>📊 CRYPTO ANALYST</h3>
        <p>Анализ трендов и курсов криптовалют в реальном времени.</p>
      </div>
      <div class="card">
        <h3>🔍 OSINT TOOLS</h3>
        <p>Поиск и агрегация информации из открытых источников.</p>
      </div>
      <div class="card">
        <h3>🎮 MINECRAFT</h3>
        <p>Честный Minecraft сервер без доната и лишних плагинов.</p>
      </div>
    </div>
  </div>
</div>

<footer>
  <p>&copy; 2025 KRIMEX DEVELOPMENT | <a href="https://t.me/krimexAI" style="color: #FFE500;">TELEGRAM</a></p>
</footer>
</body>
</html>
"""
            self._serve_html(html)

        # ---------------- УСЛУГИ ---------------- #

        elif path == "/bots":
            html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Услуги | KRIMEX</title>
  {base_styles}
</head>
<body>
{get_nav("/bots")}

<div class="hero">
  <h1>РАЗРАБОТКА БОТОВ</h1>
  <p>Создаю функциональных ботов для Telegram и Discord</p>
</div>

<div class="container">
  <div class="section">
    <h2>TELEGRAM БОТЫ</h2>
    <div class="cards">
      <div class="card">
        <h3>💰 МАГАЗИНЫ</h3>
        <p>Магазины, Web Apps, Платежки, Админки</p>
      </div>
      <div class="card">
        <h3>🤖 AI БОТЫ</h3>
        <p>Чат-боты с интеграцией GPT, Gemini, Claude</p>
      </div>
      <div class="card">
        <h3>📊 АНАЛИТИКА</h3>
        <p>Боты для мониторинга, статистики, прогнозов</p>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>DISCORD БОТЫ</h2>
    <div class="cards">
      <div class="card">
        <h3>🎮 ИГРОВЫЕ</h3>
        <p>Экономика, Модерация, Игры, Тикеты</p>
      </div>
      <div class="card">
        <h3>🛡️ МОДЕРАЦИЯ</h3>
        <p>Авто-модерация, логи, роли, верификация</p>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>ДОПОЛНИТЕЛЬНО</h2>
    <div class="cards">
      <div class="card">
        <h3>🎨 ДИЗАЙН</h3>
        <p>Красивые сайты, обложки, сервисы</p>
      </div>
      <div class="card">
        <h3>⚡ ОПТИМИЗАЦИЯ</h3>
        <p>Ускорение, рефакторинг, улучшение кода</p>
      </div>
    </div>
  </div>

  <div style="text-align: center; margin-top: 3rem;">
    <a href="https://t.me/krimexAI" class="btn">СВЯЗАТЬСЯ</a>
  </div>
</div>

<footer>
  <p>&copy; 2025 KRIMEX DEVELOPMENT | <a href="https://t.me/krimexAI" style="color: #FFE500;">TELEGRAM</a></p>
</footer>
</body>
</html>
"""
            self._serve_html(html)

        # ---------------- ХОСТИНГ ---------------- #

        elif path == "/hosting":
            html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Хостинг | KRIMEX</title>
  {base_styles}
</head>
<body>
{get_nav("/hosting")}

<div class="hero">
  <h1>ПАРТНЕРСКИЙ ХОСТИНГ</h1>
  <p>ЧЕСТНЫЕ РЕСУРСЫ. БЕЗ ОВЕРСЕЛЛИНГА.</p>
</div>

<div class="container">
  <div class="section">
    <p style="font-size: 1.2rem; text-align: center; font-weight: 700; margin-bottom: 2rem;">
      Никакого оверселлинга. Только выделенные ядра Ryzen 9 5900X для максимального FPS и скорости работы ботов.
    </p>
  </div>

  <div class="section">
    <h2>ТАРИФЫ</h2>
    <div class="pricing">
      <div class="price-card">
        <h3>STARTER</h3>
        <div class="price">399₽</div>
        <p style="margin-bottom: 1rem;">в месяц</p>
        <ul>
          <li>2 GB RAM</li>
          <li>2 vCore Ryzen 9</li>
          <li>20 GB SSD</li>
          <li>Безлимит трафика</li>
        </ul>
        <a href="https://t.me/krimexAI" class="btn" style="margin-top: 1rem;">ВЫБРАТЬ</a>
      </div>

      <div class="price-card" style="background: #FFE500;">
        <h3>PRO</h3>
        <div class="price">799₽</div>
        <p style="margin-bottom: 1rem;">в месяц</p>
        <ul>
          <li>4 GB RAM</li>
          <li>4 vCore Ryzen 9</li>
          <li>40 GB SSD</li>
          <li>Безлимит трафика</li>
        </ul>
        <a href="https://t.me/krimexAI" class="btn" style="margin-top: 1rem;">ВЫБРАТЬ</a>
      </div>

      <div class="price-card" style="background: #FF6B35;">
        <h3>ULTRA</h3>
        <div class="price">1499₽</div>
        <p style="margin-bottom: 1rem;">в месяц</p>
        <ul>
          <li>8 GB RAM</li>
          <li>6 vCore Ryzen 9</li>
          <li>80 GB SSD</li>
          <li>Безлимит трафика</li>
        </ul>
        <a href="https://t.me/krimexAI" class="btn" style="margin-top: 1rem;">ВЫБРАТЬ</a>
      </div>
    </div>
  </div>

  <div style="text-align: center; margin-top: 3rem;">
    <a href="https://t.me/krimexAI" class="btn">ВЫБРАТЬ ТАРИФ</a>
  </div>
</div>

<footer>
  <p>&copy; 2025 KRIMEX DEVELOPMENT | <a href="https://t.me/krimexAI" style="color: #FFE500;">TELEGRAM</a></p>
</footer>
</body>
</html>
"""
            self._serve_html(html)

        else:
            self.send_error(404, "Page not found")


def run_server():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"

    server_address = ("", PORT)
    httpd = ThreadingHTTPServer(server_address, SimpleHandler)
    print(f"🚀 Server running on:")
    print(f"   http://localhost:{PORT}")
    print(f"   http://{local_ip}:{PORT}")
    print(f"\n⏹  Press Ctrl+C to stop\n")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
