# TikTok Feature Generation Report
Generated on: 2025-08-30 17:05:41
Total Features: 200
Generation Seed: 42

## Label Distribution
{'Non-Compliant': 112, 'Compliant': 85, 'Partially Compliant': 3}

## Geographic Distribution
{'Netherlands': 24, 'USA-Texas': 13, 'USA-Florida': 42, 'USA-New York': 18, 'USA-California': 41, 'France': 20, 'USA-Illinois': 21, 'Germany': 21}

## Domain Distribution
{'recommendations': 29, 'advertising': 27, 'safety': 26, 'live_streaming': 30, 'privacy': 30, 'growth': 24, 'messaging': 34}

## Regulation Distribution
{'EU': 65, 'US-2258A': 52, 'US-FL': 42, 'US-CA': 41}

## Sample Features by Label

### Compliant Examples
### Compliant Examples

1. **Contextual Product Placement** (USA)
   - Domain: advertising
   - Age Range: 18-25
   - Rationale: Feature meets all US Federal CSAM Reporting Requirements (18 U.S.C. §2258A) requirements
   - Risk Tags: 

2. **Location-Based Local Ads** (USA)
   - Domain: advertising
   - Age Range: 16-18
   - Rationale: Feature meets all Florida Online Protections for Minors (HB 3) requirements
   - Risk Tags: minor_targeting, privacy_risk

3. **Friend Activity Feed** (USA)
   - Domain: recommendations
   - Age Range: 16-18
   - Rationale: Feature meets all Florida Online Protections for Minors (HB 3) requirements
   - Risk Tags: minor_targeting
### Partially Compliant Examples

1. **Granular Privacy Controls** (Netherlands)
   - Domain: privacy
   - Age Range: 18-25
   - Rationale: Partial compliance: 1 violations mitigated by clear_explanations
   - Risk Tags: addiction_risk

2. **Granular Privacy Controls** (Germany)
   - Domain: privacy
   - Age Range: 18-25
   - Rationale: Partial compliance: 1 violations mitigated by clear_explanations
   - Risk Tags: addiction_risk

3. **Granular Privacy Controls** (Germany)
   - Domain: privacy
   - Age Range: 18-25
   - Rationale: Partial compliance: 1 violations mitigated by clear_explanations
   - Risk Tags: addiction_risk
### Non-Compliant Examples

1. **Infinite Scroll for Shorts** (Netherlands)
   - Domain: recommendations
   - Age Range: 18-25
   - Rationale: Violates EU Digital Services Act (DSA): Recommender systems without transparency/control options
   - Risk Tags: addiction_risk, high_risk_feature

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
