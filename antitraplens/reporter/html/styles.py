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

.tabs {
    margin-bottom: 25px;
}

.tab-buttons {
    display: flex;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;
}

.tab-button {
    background: none;
    border: none;
    padding: 12px 24px;
    cursor: pointer;
    font-size: 1em;
    font-weight: 500;
    color: #666666;
    border-bottom: 2px solid transparent;
    transition: all 0.3s ease;
}

.tab-button.active {
    color: #000000;
    border-bottom-color: #000000;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.tracking-warning {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    border: 2px solid #f44336;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(244, 67, 54, 0.2);
}

.tracking-warning h3 {
    color: #d32f2f;
    font-size: 1.4em;
    margin-bottom: 10px;
    font-weight: 600;
}

.warning-text {
    color: #d32f2f;
    font-size: 1.1em;
    margin-bottom: 15px;
    font-weight: 500;
}

.tracking-domains h4 {
    color: #d32f2f;
    font-size: 1.1em;
    margin-bottom: 10px;
    font-weight: 500;
}

.domain-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tracking-domain {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 0.9em;
    color: #333333;
    font-weight: 500;
    white-space: nowrap;
}

.tracking-domain.more {
    background: #f5f5f5;
    color: #666666;
    font-style: italic;
}

.project-header {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    color: #ffffff;
    padding: 20px 0;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.project-info h1 {
    font-size: 2.5em;
    font-weight: 300;
    margin-bottom: 10px;
    letter-spacing: 2px;
}

.project-info p {
    font-size: 1.2em;
    margin-bottom: 15px;
    opacity: 0.9;
}

.author-info {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    font-size: 0.9em;
}

.github-link {
    color: #4CAF50;
    text-decoration: none;
    padding: 8px 16px;
    border: 1px solid #4CAF50;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.github-link:hover {
    background: #4CAF50;
    color: white;
}

.analysis-section {
    margin-bottom: 30px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #007bff;
}

.dark-patterns-section {
    border-left-color: #dc3545;
}

.cookies-section {
    border-left-color: #ffc107;
}

.section-title {
    font-size: 1.3em;
    font-weight: 600;
    margin-bottom: 15px;
    color: #333;
}

.tracking-notice {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 20px;
}

.tracking-notice .warning-text {
    color: #856404;
    font-weight: 500;
    margin: 0;
}

.project-footer {
    background: #2d2d2d;
    color: #ffffff;
    padding: 30px 0;
    margin-top: 60px;
    text-align: center;
}

.footer-content p {
    margin: 5px 0;
    opacity: 0.8;
}

.footer-content a {
    color: #4CAF50;
    text-decoration: none;
}

.footer-content a:hover {
    text-decoration: underline;
}

.tracking-summary {
    margin: 15px 0;
}

.summary-stats {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 15px;
}

.stat {
    background: rgba(255, 255, 255, 0.8);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 500;
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.stat.known-trackers {
    background: #e3f2fd;
    color: #1976d2;
    border-color: #1976d2;
}

.stat.potential-trackers {
    background: #fff3e0;
    color: #f57c00;
    border-color: #f57c00;
}

.stat.high-risk {
    background: #ffebee;
    color: #d32f2f;
    border-color: #d32f2f;
}

.tracking-domain.risk-high {
    background: #ffebee;
    border-color: #f44336;
    color: #d32f2f;
    font-weight: 600;
}

.tracking-domain.risk-medium {
    background: #fff3e0;
    border-color: #ff9800;
    color: #f57c00;
}

.tracking-domain.risk-low {
    background: #e8f5e8;
    border-color: #4caf50;
    color: #2e7d32;
}

.tracking-domain.risk-minimal {
    background: #f5f5f5;
    border-color: #9e9e9e;
    color: #616161;
}

.data-sharing-notice {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    margin-top: 15px;
}

.data-sharing-notice p {
    color: #d32f2f;
    font-weight: 600;
    margin-bottom: 10px;
}

.data-sharing-list {
    list-style: none;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 5px;
}

.data-sharing-list li {
    background: #f8f8f8;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 0.9em;
    color: #333;
    border: 1px solid #e0e0e0;
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

/* Enhanced layout styles */
.page-meta {
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
}

.page-title {
    font-size: 0.9em;
    color: #666;
    font-weight: normal;
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.section-description {
    background: #f8f9fa;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 20px;
    font-size: 0.9em;
    color: #555;
    border-left: 3px solid #007bff;
}

.finding-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.severity-badge {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75em;
    font-weight: bold;
    text-transform: uppercase;
}

.severity-badge.severity-high {
    background: #dc3545;
    color: white;
}

.severity-badge.severity-medium {
    background: #ffc107;
    color: #212529;
}

.severity-badge.severity-low {
    background: #28a745;
    color: white;
}

.finding-description {
    color: #333;
    margin-bottom: 8px;
    font-style: italic;
}

.pattern-explanation {
    background: #e8f4f8;
    padding: 8px 12px;
    border-radius: 4px;
    margin-bottom: 6px;
    font-size: 0.9em;
    border-left: 3px solid #17a2b8;
}

.user-impact {
    background: #fff3cd;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 0.9em;
    border-left: 3px solid #ffc107;
    color: #856404;
}

.summary-subsection {
    margin-bottom: 40px;
}

.section-intro {
    color: #666;
    margin-bottom: 20px;
    font-style: italic;
}

.summary-card .pattern-description {
    font-size: 0.8em;
    color: #666;
    margin-top: 8px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.cookie-findings {
    margin-top: 20px;
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.cookie-findings h4 {
    color: #e67e22;
    margin-bottom: 15px;
}
"""
