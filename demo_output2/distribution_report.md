# TikTok Feature Generation Report
Generated on: 2025-08-30 17:04:46
Total Features: 50
Generation Seed: 789

## Label Distribution
{'Compliant': 25, 'Non-Compliant': 24, 'Partially Compliant': 1}

## Geographic Distribution
{'France': 10, 'USA-California': 15, 'USA-Florida': 16, 'Netherlands': 3, 'Germany': 6}

## Domain Distribution
{'safety': 7, 'privacy': 7, 'growth': 5, 'recommendations': 13, 'messaging': 6, 'advertising': 4, 'live_streaming': 8}

## Regulation Distribution
{'EU': 19, 'US-CA': 15, 'US-FL': 16}

## Sample Features by Label

### Compliant Examples
### Compliant Examples

1. **Crisis Intervention Alerts** (France)
   - Domain: safety
   - Age Range: 18-25
   - Rationale: Feature meets all EU Digital Services Act (DSA) requirements
   - Risk Tags: 

2. **Data Download Portal** (USA)
   - Domain: privacy
   - Age Range: 14-16
   - Rationale: Feature meets all California Protecting Our Kids from Social Media Addiction Act requirements
   - Risk Tags: minor_targeting, addiction_risk

3. **Minor Direct Messaging** (USA)
   - Domain: messaging
   - Age Range: 18-65
   - Rationale: Feature meets all Florida Online Protections for Minors (HB 3) requirements
   - Risk Tags: high_risk_feature
### Partially Compliant Examples

1. **Personalized Study Feed** (USA)
   - Domain: recommendations
   - Age Range: 21-65
   - Rationale: Partial compliance: 1 violations mitigated by time_limits
   - Risk Tags: addiction_risk
### Non-Compliant Examples

1. **Automatic Data Deletion** (USA)
   - Domain: privacy
   - Age Range: 13-18
   - Rationale: Violates Florida Online Protections for Minors (HB 3): Targets users under 14 (banned in Florida)
   - Risk Tags: child_targeting

2. **Social Proof Metrics** (USA)
   - Domain: growth
   - Age Range: 14-16
   - Rationale: Violates California Protecting Our Kids from Social Media Addiction Act: Algorithmic features without proper user controls
   - Risk Tags: minor_targeting, addiction_risk

3. **Auto-play Next Video** (USA)
   - Domain: recommendations
   - Age Range: 13-15
   - Rationale: Violates California Protecting Our Kids from Social Media Addiction Act: Algorithmic features without proper user controls
   - Risk Tags: child_targeting, addiction_risk, high_risk_feature
