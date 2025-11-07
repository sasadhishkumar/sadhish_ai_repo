# playwright_demo.py
from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def get_ind_vs_aus_score():
    score_file = "score.txt"  # File to save score
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)  # Change to True for no window
        page = browser.new_page()

        try:
            print("Going to Cricbuzz...") 
            page.goto("https://www.cricbuzz.com")

            print("Searching: India vs Australia")
            page.fill("input[placeholder='Search for Team, Player or Series']", "India vs Australia")
            page.press("input[placeholder='Search for Team, Player or Series']", "Enter")

            page.wait_for_selector("a[href*='cricket-match']", timeout=15000)

            match = page.query_selector("a:has-text('IND'):has-text('AUS')") or \
                    page.query_selector("a:has-text('India'):has-text('Australia')")

            if match:
                match.click()
                page.wait_for_load_state("networkidle")
                time.sleep(3)

                score_elem = page.locator(".cbz-scorecard-title, .cb-col-100.cb-lv-scrs-col, .cb-lv-scrs-col").first
                if score_elem and score_elem.inner_text().strip():
                    score_text = score_elem.inner_text().strip()
                    
                    # Current time in IST
                    now = datetime.now().strftime("%Y-%m-%d %I:%M %p IST")

                    # Print to terminal
                    print("\n" + "="*60)
                    print("INDIA vs AUSTRALIA - LIVE SCORE")
                    print("="*60)
                    print(score_text)
                    print(f"Updated: {now}")
                    print("="*60)

                    # SAVE TO score.txt
                    with open(score_file, "w", encoding="utf-8") as f:
                        f.write("INDIA vs AUSTRALIA - LIVE SCORE\n")
                        f.write("="*60 + "\n")
                        f.write(score_text + "\n")
                        f.write(f"Updated: {now}\n")
                        f.write("="*60 + "\n")
                    print(f"\nScore saved to {score_file}")
                else:
                    message = "Score not found on page."
                    print(message)
                    with open(score_file, "w") as f:
                        f.write(message + "\n")
            else:
                message = "No live India vs Australia match found."
                print(message)
                with open(score_file, "w") as f:
                    f.write(message + "\n")

            # AUTO-CLOSE AFTER 10 SECONDS
            print("\nBrowser will auto-close in 10 seconds...")
            time.sleep(10)

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            with open(score_file, "w") as f:
                f.write(error_msg + "\n")
        finally:
            print("Closing browser...")
            browser.close()

if __name__ == "__main__":
    get_ind_vs_aus_score()