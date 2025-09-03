"""
CSS styles for HTML reports.
"""

CSS_STYLES = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #ffffff;
    color: #000000;
    line-height: 1.6;
}

.hero-section {
    position: relative;
    height: 400px;
    background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
    overflow: hidden;
}

.hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 40px;
    text-align: center;
}

.logo {
    font-size: 2.5em;
    font-weight: 300;
    letter-spacing: 2px;
    margin-bottom: 20px;
    color: #000000;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.hero-title {
    font-size: 3em;
    font-weight: 200;
    margin-bottom: 40px;
    color: #000000;
    max-width: 800px;
    line-height: 1.2;
}

.hero-stats {
    display: flex;
    gap: 60px;
    margin-top: 30px;
}

.stat-item {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 2.5em;
    font-weight: 300;
    color: #000000;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9em;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 40px;
}

.pages-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 40px;
    margin-bottom: 80px;
}

.page-card {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.page-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card-variation-1 { min-height: 450px; }
.card-variation-2 { min-height: 380px; }
.card-variation-3 { min-height: 420px; }

.card-header {
    background: linear-gradient(135deg, #f8f8f8 0%, #ffffff 100%);
    padding: 30px 30px 20px;
    border-bottom: 1px solid #e0e0e0;
}

.card-header h3 {
    font-size: 1.5em;
    font-weight: 400;
    color: #000000;
    margin-bottom: 15px;
}

.category-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.category-general { background: #000000; color: #ffffff; }
.category-ecommerce { background: #333333; color: #ffffff; }
.category-social { background: #666666; color: #ffffff; }

.card-content {
    padding: 30px;
}

.url-display {
    margin-bottom: 25px;
}

.url-link {
    color: #000000;
    text-decoration: none;
    font-weight: 500;
    border-bottom: 1px solid #000000;
    transition: border-color 0.3s ease;
}

.url-link:hover {
    border-color: #666666;
}

.cookies, .findings, .score {
    margin-bottom: 25px;
}

.cookies h4, .findings h4, .score h4 {
    font-size: 1.1em;
    font-weight: 500;
    color: #000000;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.findings ul {
    list-style: none;
    padding: 0;
}

.finding {
    background: #f8f8f8;
    padding: 15px 20px;
    margin-bottom: 10px;
    border-radius: 8px;
    border-left: 4px solid #000000;
    font-size: 0.9em;
}

.severity-high { border-left-color: #000000; background: #f0f0f0; }
.severity-medium { border-left-color: #666666; background: #f8f8f8; }
.severity-low { border-left-color: #cccccc; background: #fafafa; }

.grade {
    font-size: 1.4em;
    font-weight: 300;
    padding: 12px 24px;
    border-radius: 25px;
    display: inline-block;
}

.grade-a, .grade-b { background: #000000; color: #ffffff; }
.grade-c { background: #666666; color: #ffffff; }
.grade-d, .grade-f { background: #333333; color: #ffffff; }

.summary-section {
    background: #f8f8f8;
    padding: 60px 0;
    margin-top: 80px;
}

.summary-section h2 {
    text-align: center;
    font-size: 2.5em;
    font-weight: 200;
    color: #000000;
    margin-bottom: 50px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 40px;
}

.summary-card {
    background: #ffffff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease;
}

.summary-card:hover {
    transform: translateY(-3px);
}

.pattern-name {
    font-size: 1.2em;
    font-weight: 400;
    color: #000000;
    margin-bottom: 15px;
}

.pattern-count {
    font-size: 3em;
    font-weight: 200;
    color: #000000;
    margin-bottom: 10px;
}

.pattern-severity {
    font-size: 0.9em;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.severity-high .pattern-severity { color: #000000; }
.severity-medium .pattern-severity { color: #666666; }
.severity-low .pattern-severity { color: #cccccc; }

.no-findings {
    text-align: center;
    font-size: 1.5em;
    color: #666666;
    padding: 60px;
    font-style: italic;
}

@media (max-width: 768px) {
    .hero-stats {
        flex-direction: column;
        gap: 30px;
    }

    .pages-section {
        grid-template-columns: 1fr;
        gap: 30px;
    }

    .summary-grid {
        grid-template-columns: 1fr;
        padding: 0 20px;
    }

    .hero-title {
        font-size: 2em;
    }

    .content-wrapper {
        padding: 40px 20px;
    }
}
"""
