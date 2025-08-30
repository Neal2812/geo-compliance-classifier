# TikTok Feature Generation Report
Generated on: 2025-08-30 16:00:58
Total Features: 50
Generation Seed: 42

## Label Distribution
{'Compliant': 31, 'Non-Compliant': 17, 'Partially Compliant': 2}

## Geographic Distribution
{'Germany': 8, 'Netherlands': 7, 'USA-California': 12, 'USA-Florida': 16, 'France': 7}

## Domain Distribution
{'recommendations': 11, 'advertising': 7, 'growth': 5, 'privacy': 4, 'safety': 10, 'live_streaming': 5, 'messaging': 8}

## Regulation Distribution
{'EU': 15, 'US-2258A': 7, 'US-CA': 12, 'US-FL': 16}

## Sample Features by Label

### Compliant Examples
### Compliant Examples

1. **Infinite Scroll for Shorts** (Germany)
   - Domain: recommendations
   - Age Range: 18-25
   - Rationale: Feature meets all EU Digital Services Act (DSA) requirements
   - Risk Tags: addiction_risk, high_risk_feature

2. **Contextual Product Placement** (Netherlands)
   - Domain: advertising
   - Age Range: 18-25
   - Rationale: Feature meets all US Federal CSAM Reporting Requirements (18 U.S.C. §2258A) requirements
   - Risk Tags: 

3. **Gamified Achievement System** (USA)
   - Domain: growth
   - Age Range: 16-18
   - Rationale: Feature meets all California Protecting Our Kids from Social Media Addiction Act requirements
   - Risk Tags: minor_targeting, high_risk_feature
### Partially Compliant Examples

1. **Minor Direct Messaging** (USA)
   - Domain: messaging
   - Age Range: 18-25
   - Rationale: Partial compliance: 1 violations mitigated by parental_oversight
   - Risk Tags: addiction_risk, high_risk_feature

2. **Minor Direct Messaging** (USA)
   - Domain: messaging
   - Age Range: 14-17
   - Rationale: Partial compliance: 2 violations mitigated by parental_oversight
   - Risk Tags: minor_targeting, addiction_risk, high_risk_feature
### Non-Compliant Examples

1. **Granular Privacy Controls** (USA)
   - Domain: privacy
   - Age Range: 14-17
   - Rationale: Violates Florida Online Protections for Minors (HB 3): Missing parental consent for 14-15 age group
   - Risk Tags: minor_targeting

2. **Crisis Intervention Alerts** (USA)
   - Domain: safety
   - Age Range: 16-18
   - Rationale: Violates Florida Online Protections for Minors (HB 3): Uses addictive feature: push_notifications
   - Risk Tags: minor_targeting, addiction_risk

3. **Cyberbullying Detection** (USA)
   - Domain: safety
   - Age Range: 14-16
   - Rationale: Violates Florida Online Protections for Minors (HB 3): Missing parental consent for 14-15 age group; Uses addictive feature: infinite_scroll; Uses addictive feature: variable_rewards
   - Risk Tags: minor_targeting, addiction_risk
