# Sub-Agent Capabilities Guide

**Nomark Project — Internal Document**

---

## What Sub-Agents CAN Do ✅

### 1. Research & Information Gathering
- Search the web for brands, contacts, partnerships
- Fetch articles and content from URLs
- Compile lists of companies, emails, application links
- Find news, press coverage, social media stats

### 2. Content Creation
- Write articles, blog posts, op-eds
- Draft pitch emails and outreach templates
- Create social media content
- Write summaries and reports

### 3. File Management
- Create, read, edit, and save files
- Organize folders and documents
- Backup and sync to GitHub

### 4. Data Processing
- Compile and format lists
- Organize research findings
- Generate reports

### 5. Simple Automation
- Run predefined scripts
- Execute backup commands
- Schedule tasks (within their session)

---

## What Sub-Agents CANNOT Do ❌

### 1. Account Creation
- Cannot create Gmail, social media, or platform accounts
- Most platforms require phone/SMS verification
- Cannot pass CAPTCHAs or human verification checks

### 2. Sending External Communications
- Cannot send real emails (need email server/SMTP config)
- Cannot send DMs on platforms outside configured channels
- Cannot access external APIs without credentials

### 3. Persistent System Changes
- Cannot install system packages reliably
- Cannot configure cron jobs or system services
- Cannot modify system configurations

### 4. Physical Actions
- Cannot interact with physical hardware
- Cannot handle physical products or shipping

### 5. Financial Transactions
- Cannot process payments
- Cannot access bank accounts or payment systems

### 6. Real-Time Platform Interactions
- Cannot log into Instagram/TikTok/YouTube to post
- Cannot manage social media accounts directly
- Cannot respond to comments/DMs in real-time

---

## What Would Enable Sub-Agents to Do More 🔧

### For Account Creation:
- **Need:** Phone number verification service (like SMS-activate)
- **Or:** Human in the loop to handle verification steps

### For Sending Emails:
- **Need:** SMTP server credentials OR Gmail API access
- **Or:** Use configured email channel through OpenClaw

### For Social Media Management:
- **Need:** Official Meta/TikTok/YouTube API credentials
- **Or:** Third-party social media management tool credentials

### For System Changes:
- **Need:** Root/sudo access with proper permissions
- **Or:** Pre-configured scripts that don't require system changes

### For Real-Time Interactions:
- **Need:** Browser automation with logged-in sessions
- **Or:** API access to platforms for automated posting

---

## Summary

| Capability | Can Do | Cannot Do |
|------------|--------|-----------|
| Research | ✅ | - |
| Content Writing | ✅ | - |
| File Management | ✅ | - |
| Sending Emails | ❌ | Need SMTP/API |
| Account Creation | ❌ | Need phone verification |
| System Config | ❌ | Need sudo + approval |
| Social Media Posting | ❌ | Need API credentials |

---

*Document created: April 7, 2026*
*For Nomark Project internal use*