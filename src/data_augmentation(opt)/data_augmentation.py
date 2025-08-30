#!/usr/bin/env python3
"""
Feature Data Augmentation for Geo-Compliance Classification

This script generates synthetic feature descriptions in the same format as feature_sample_data.csv:
- feature_name: Short descriptive name
- feature_description: Detailed description using internal codenames and compliance terminology

Generates realistic social media platform features with:
- Internal codenames (ASL, GH, CDS, T5, etc.)
- Compliance requirements for various jurisdictions
- Technical implementation details
- Safety and privacy considerations
"""

import csv
import random
import json
from typing import List, Dict, Tuple
from collections import defaultdict

# Set random seed for reproducibility
random.seed(42)

class FeatureDataGenerator:
    """Generate synthetic feature data in the same format as feature_sample_data.csv"""
    
    def __init__(self):
        # Load terminology from the existing terminology.csv
        self.codenames = {
            'NR': 'Not recommended',
            'PF': 'Personalized feed', 
            'GH': 'Geo-handler',
            'CDS': 'Compliance Detection System',
            'DRT': 'Data retention threshold',
            'LCP': 'Local compliance policy',
            'Redline': 'Flag for legal review',
            'Softblock': 'User limitation applied silently',
            'Spanner': 'Rule engine',
            'ShadowMode': 'Non-user-impact analytics deployment',
            'T5': 'Tier 5 sensitivity data',
            'ASL': 'Age-sensitive logic',
            'Glow': 'Compliance-flagging status',
            'NSP': 'Non-shareable policy',
            'Jellybean': 'Parental control system',
            'EchoTrace': 'Log tracing mode',
            'BB': 'Baseline Behavior',
            'Snowcap': 'Child safety policy framework',
            'FR': 'Feature rollout status',
            'IMT': 'Internal monitoring trigger'
        }
        
        self.jurisdictions = {
            'US': ['Utah', 'California', 'Florida', 'Texas', 'New York', 'Washington'],
            'EU': ['Germany', 'France', 'Netherlands', 'Italy', 'Spain', 'Belgium'],
            'Other': ['Canada', 'United Kingdom', 'Australia', 'South Korea', 'Japan', 'Brazil']
        }
        
        self.regulations = {
            'Utah': 'Utah Social Media Regulation Act',
            'California': "California's SB976",
            'Florida': "Florida's Online Protections for Minors law",
            'Texas': 'Texas SCOPE Act',
            'EU': 'EU Digital Services Act',
            'Germany': 'German Network Enforcement Act',
            'US Federal': 'COPPA compliance requirements',
            'GDPR': 'General Data Protection Regulation'
        }
        
        self.feature_types = [
            'login restriction', 'content filtering', 'parental control', 'age verification',
            'data retention', 'notification system', 'content moderation', 'user safety',
            'privacy protection', 'analytics tracking', 'feed customization', 'chat feature',
            'video feature', 'social feature', 'monetization feature', 'profile feature'
        ]
        
        self.feature_actions = [
            'blocking', 'limiting', 'monitoring', 'filtering', 'restricting', 'enabling',
            'disabling', 'tracking', 'logging', 'flagging', 'scanning', 'detecting',
            'controlling', 'managing', 'routing', 'triggering', 'enforcing', 'auditing'
        ]
        
        self.compliance_reasons = [
            'age verification requirements',
            'parental consent obligations', 
            'data protection standards',
            'content safety measures',
            'privacy transparency',
            'minor protection laws',
            'content reporting requirements',
            'user safety protocols',
            'geographical compliance',
            'retention policy enforcement'
        ]
    
    def generate_feature_name(self) -> str:
        """Generate a realistic feature name"""
        components = [
            random.choice(self.feature_types),
            'with',
            random.choice(list(self.codenames.keys())),
            'and',
            random.choice(list(self.codenames.keys())),
            'for',
            random.choice([
                f"{random.choice(self.jurisdictions['US'])} minors",
                f"{random.choice(self.jurisdictions['EU'])} users", 
                f"{random.choice(self.jurisdictions['Other'])} compliance",
                "underage users",
                "teen safety",
                "parental controls"
            ])
        ]
        
        # Sometimes use simpler names
        if random.random() < 0.4:
            components = [
                random.choice([
                    random.choice(list(self.codenames.keys())),
                    f"{random.choice(self.feature_actions)} {random.choice(self.feature_types)}"
                ]),
                random.choice(['auto-flagging', 'enforcement', 'detection', 'controls', 'monitoring'])
            ]
        
        return ' '.join(components)
    
    def generate_feature_description(self, feature_name: str) -> str:
        """Generate a detailed feature description with codenames and compliance context"""
        
        # Choose jurisdiction and regulation
        region = random.choice(['US', 'EU', 'Other'])
        if region == 'US':
            jurisdiction = random.choice(self.jurisdictions['US'])
            regulation = self.regulations.get(jurisdiction, 'state privacy laws')
        elif region == 'EU':
            jurisdiction = random.choice(self.jurisdictions['EU'])
            regulation = random.choice([self.regulations['EU'], self.regulations['GDPR']])
        else:
            jurisdiction = random.choice(self.jurisdictions['Other'])
            regulation = 'local data protection requirements'
        
        # Choose compliance context
        compliance_context = random.choice([
            f"To comply with the {regulation}",
            f"In line with {jurisdiction} {random.choice(self.compliance_reasons)}",
            f"To meet the {random.choice(self.compliance_reasons)} of the {regulation}",
            f"As part of compliance with {regulation}",
            f"To support {regulation}"
        ])
        
        # Choose technical implementation
        codename1 = random.choice(list(self.codenames.keys()))
        codename2 = random.choice(list(self.codenames.keys()))
        codename3 = random.choice(list(self.codenames.keys()))
        
        technical_details = [
            f"The system uses {codename1} to {random.choice(['detect', 'segment', 'filter', 'route', 'monitor'])} {random.choice(['user accounts', 'content', 'behaviors', 'violations', 'activities'])}",
            f"Routes enforcement through {codename2} to apply only within {jurisdiction} boundaries",
            f"Uses {codename3} for {random.choice(['auditability', 'traceability', 'monitoring', 'compliance validation', 'safety checks'])}",
            f"Operating in {random.choice(['ShadowMode', 'Spanner', 'EchoTrace'])} during {random.choice(['initial rollout', 'testing phase', 'validation period'])}"
        ]
        
        # Additional implementation details
        additional_details = [
            f"The feature {random.choice(['activates', 'triggers', 'applies', 'enforces'])} during {random.choice(['restricted hours', 'specific conditions', 'policy violations', 'safety events'])}",
            f"Logs activity using {random.choice(['EchoTrace', 'CDS', 'FR', 'IMT'])} for {random.choice(['auditability', 'compliance tracking', 'safety monitoring'])}",
            f"This allows {random.choice(['parental control', 'safety measures', 'compliance enforcement', 'privacy protection'])} to be {random.choice(['enacted', 'implemented', 'maintained'])} without {random.choice(['user-facing alerts', 'service disruption', 'privacy concerns'])}",
            f"The design ensures {random.choice(['minimal disruption', 'compliance accuracy', 'user safety', 'privacy protection'])} while meeting the {random.choice(['strict requirements', 'regulatory standards', 'safety protocols'])} imposed by the law"
        ]
        
        # Build description
        description_parts = [
            compliance_context + ",",
            random.choice([
                f"we are implementing a {random.choice(self.feature_types)} for {random.choice(['users under 18', 'minor accounts', 'teen users', 'underage profiles'])}.",
                f"this feature {random.choice(['scans', 'monitors', 'filters', 'controls', 'manages'])} {random.choice(['uploads', 'content', 'user activity', 'interactions', 'behaviors'])} and {random.choice(['flags', 'blocks', 'restricts', 'routes', 'logs'])} {random.choice(['suspected materials', 'policy violations', 'safety risks', 'compliance issues'])}.",
                f"the app will {random.choice(['disable', 'enable', 'restrict', 'monitor', 'control'])} {random.choice(['PF', 'content sharing', 'messaging features', 'social features'])} by default for {random.choice(['users under 18', 'minor accounts', 'teen profiles'])} located in {jurisdiction}."
            ]),
            random.choice(technical_details) + ".",
            random.choice(additional_details) + ".",
            random.choice([
                f"{random.choice(['Regional', 'Geographic', 'Compliance'])} {random.choice(['thresholds', 'parameters', 'controls'])} are governed by {random.choice(['LCP', 'DRT', 'Spanner'])} parameters in the backend.",
                f"{random.choice(['Glow', 'Redline', 'FR'])} flags ensure {random.choice(['compliance visibility', 'safety monitoring', 'audit tracking'])} during rollout phases.",
                f"The logic runs in {random.choice(['real-time', 'batch mode', 'continuous mode'])}, supports {random.choice(['human validation', 'automated review', 'compliance checks'])}, and logs {random.choice(['detection metadata', 'compliance events', 'safety metrics'])} for internal audits."
            ])
        ]
        
        return " ".join(description_parts)
    
    def generate_features(self, count: int = 50) -> List[Tuple[str, str]]:
        """Generate a list of synthetic features"""
        features = []
        
        for _ in range(count):
            feature_name = self.generate_feature_name()
            feature_description = self.generate_feature_description(feature_name)
            features.append((feature_name, feature_description))
        
        return features
    
    def save_to_csv(self, features: List[Tuple[str, str]], filepath: str):
        """Save features to CSV file in the same format as feature_sample_data.csv"""
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['feature_name', 'feature_description'])
            for feature_name, feature_description in features:
                writer.writerow([feature_name, feature_description])
        
        print(f"💾 Saved {len(features)} features to {filepath}")
    
    def generate_augmentation_report(self, features: List[Tuple[str, str]]) -> str:
        """Generate a report about the generated features"""
        codename_usage = defaultdict(int)
        jurisdiction_usage = defaultdict(int)
        
        for name, description in features:
            # Count codename usage
            for codename in self.codenames.keys():
                if codename in description:
                    codename_usage[codename] += 1
            
            # Count jurisdiction mentions
            for jurisdictions in self.jurisdictions.values():
                for jurisdiction in jurisdictions:
                    if jurisdiction in description:
                        jurisdiction_usage[jurisdiction] += 1
        
        report = f"""# Feature Data Augmentation Report
Generated: {count} synthetic features

## Codename Usage Distribution
"""
        for codename, count in sorted(codename_usage.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{codename}**: {count} features ({self.codenames[codename]})\n"
        
        report += f"""
## Jurisdiction Coverage
"""
        for jurisdiction, count in sorted(jurisdiction_usage.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                report += f"- **{jurisdiction}**: {count} features\n"
        
        report += f"""
## Feature Categories Generated
- Age verification and parental controls
- Content moderation and safety
- Data retention and privacy
- Geographic compliance enforcement
- User behavior monitoring
- Feed and recommendation controls

## Quality Measures
- Realistic internal codename usage
- Jurisdiction-specific compliance references
- Technical implementation details
- Safety and privacy considerations
- Regulatory framework alignment
"""
        
        return report
        
        def main():
    """Main feature generation pipeline"""
    print("🚀 Feature Data Generation Pipeline")
    print("=" * 60)
    
    # Initialize generator
    generator = FeatureDataGenerator()
    
    # Generate features
    print("🔄 Generating synthetic features...")
    features = generator.generate_features(count=100)  # Generate 100 features
    
    # Save to CSV
    output_path = 'generated_output/augmented_features.csv'
    generator.save_to_csv(features, output_path)
    
    # Generate report
    report = generator.generate_augmentation_report(features)
    report_path = 'generated_output/feature_generation_report.md'
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"✅ Generated {len(features)} features")
    print(f"📄 Report saved to: {report_path}")
    print(f"📁 Features saved to: {output_path}")
    
    # Display sample features
    print("
🔍 Sample Generated Features:")
    print("-" * 40)
    for i, (name, description) in enumerate(features[:3]):
        print(f"
**Feature {i+1}:** {name}")
        print(f"**Description:** {description[:200]}...")
    
    return features

if __name__ == "__main__":
    main()
        
        self.feature_types = [
            'Social Media', 'User Registration', 'Content Sharing', 'Messaging', 'Live Streaming',
            'Gaming', 'E-commerce', 'Educational Platform', 'Dating App', 'News Platform',
            'Video Platform', 'Photo Sharing', 'Professional Network', 'Forum', 'Chat App'
        ]
    
    def load_data(self, filepath: str) -> List[Dict]:
        """Load the original corrections dataset."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def analyze_dataset(self, data: List[Dict]) -> Dict:
        """Analyze dataset for augmentation planning."""
        analysis = {
            'total_records': len(data),
            'label_distribution': Counter(item['corrected_label'] for item in data),
            'regulation_distribution': Counter(item['feature_characteristics']['regulation_type'] for item in data),
            'geographic_distribution': defaultdict(int),
            'confidence_stats': {
                'min': min(item['confidence_score'] for item in data),
                'max': max(item['confidence_score'] for item in data),
                'avg': sum(item['confidence_score'] for item in data) / len(data)
            }
        }
        
        # Geographic analysis
        for item in data:
            geo = item['feature_characteristics']['geographic']
            if 'country' in geo:
                analysis['geographic_distribution'][geo['country']] += 1
            elif 'region' in geo:
                analysis['geographic_distribution'][geo['region']] += 1
                
        return analysis
    
    def generate_synthetic_reasoning(self, regulation_type: str, geo_info: Dict, demographics: Dict) -> str:
        """Generate realistic reviewer reasoning using templates."""
        if regulation_type not in self.regulation_patterns:
            return f"Feature violates {regulation_type} requirements in specified jurisdiction"
        
        patterns = self.regulation_patterns[regulation_type]
        template = random.choice(patterns['reasoning_templates'])
        
        # Fill template variables
        if '{age}' in template:
            age = demographics.get('age_max', 18)
            template = template.replace('{age}', str(age))
        
        if '{age_group}' in template:
            age_min = demographics.get('age_min', 13)
            age_max = demographics.get('age_max', 17)
            template = template.replace('{age_group}', f"{age_min}-{age_max}")
        
        if '{jurisdiction}' in template:
            jurisdiction = geo_info.get('country', geo_info.get('region', 'local'))
            template = template.replace('{jurisdiction}', jurisdiction)
        
        # Add regulation-specific variables
        for key, values in patterns.items():
            if key != 'reasoning_templates' and f'{{{key[:-1]}}}' in template:
                value = random.choice(values)
                template = template.replace(f'{{{key[:-1]}}}', str(value))
        
        return template
    
    def create_geographic_variant(self, original: Dict, target_jurisdiction: str) -> Dict:
        """Create geographic variant by adapting to similar jurisdiction."""
        variant = copy.deepcopy(original)
        
        # Update case ID and timestamp
        variant['case_id'] = f"AUG-{uuid.uuid4().hex[:8]}"
        variant['timestamp'] = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        
        # Update geographic information
        if target_jurisdiction in self.jurisdiction_mappings:
            mapping = self.jurisdiction_mappings[target_jurisdiction]
            
            if target_jurisdiction == 'USA':
                state = random.choice(mapping['similar_states'])
                variant['feature_characteristics']['geographic'] = {
                    'state': state,
                    'country': 'USA'
                }
            else:
                variant['feature_characteristics']['geographic'] = {
                    'country': target_jurisdiction,
                    'region': random.choice(mapping['regions'])
                }
        
        # Slightly adjust confidence score
        confidence_delta = random.uniform(-0.1, 0.1)
        new_confidence = max(0.1, min(0.99, variant['confidence_score'] + confidence_delta))
        variant['confidence_score'] = round(new_confidence, 2)
        
        # Update reasoning to reflect new jurisdiction
        reg_type = variant['feature_characteristics']['regulation_type']
        geo_info = variant['feature_characteristics']['geographic']
        demographics = variant['feature_characteristics']['demographic']
        
        variant['reviewer_reasoning'] = self.generate_synthetic_reasoning(reg_type, geo_info, demographics)
        
        return variant
    
    def create_temporal_variant(self, original: Dict) -> Dict:
        """Create temporal variant with different compliance timeline."""
        variant = copy.deepcopy(original)
        
        # Update identifiers
        variant['case_id'] = f"AUG-{uuid.uuid4().hex[:8]}"
        variant['timestamp'] = (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
        
        # Adjust age ranges slightly
        demo = variant['feature_characteristics']['demographic']
        if 'age_min' in demo and 'age_max' in demo:
            age_shift = random.choice([-1, 0, 1])
            demo['age_min'] = max(13, demo['age_min'] + age_shift)
            demo['age_max'] = min(65, demo['age_max'] + age_shift)
        
        # Adjust confidence and impact scores
        variant['confidence_score'] = round(random.uniform(0.7, 0.95), 2)
        variant['impact_score'] = round(random.uniform(0.6, 0.9), 2)
        
        # Update feature type occasionally
        if random.random() < 0.3:
            variant['feature_characteristics']['feature_type'] = random.choice(self.feature_types)
        
        return variant
    
    def create_regulation_variant(self, original: Dict, target_regulation: str) -> Dict:
        """Create variant by adapting to different but related regulation type."""
        variant = copy.deepcopy(original)
        
        # Update identifiers
        variant['case_id'] = f"AUG-{uuid.uuid4().hex[:8]}"
        variant['timestamp'] = (datetime.now() - timedelta(days=random.randint(1, 45))).isoformat()
        
        # Update regulation type
        variant['feature_characteristics']['regulation_type'] = target_regulation
        
        # Generate new reasoning
        geo_info = variant['feature_characteristics']['geographic']
        demographics = variant['feature_characteristics']['demographic']
        variant['reviewer_reasoning'] = self.generate_synthetic_reasoning(target_regulation, geo_info, demographics)
        
        # Adjust confidence based on regulation complexity
        complexity_map = {
            'Age Verification': 0.85,
            'Data Protection': 0.75,
            'Privacy': 0.80,
            'Safety': 0.90,
            'Parental Consent': 0.85
        }
        base_confidence = complexity_map.get(target_regulation, 0.80)
        variant['confidence_score'] = round(random.uniform(base_confidence - 0.1, base_confidence + 0.1), 2)
        
        return variant
    
    def balance_compliant_samples(self, data: List[Dict], target_ratio: float = 0.3) -> List[Dict]:
        """Create compliant samples to balance the dataset."""
        non_compliant = [item for item in data if item['corrected_label'] == 'Non-Compliant']
        compliant = [item for item in data if item['corrected_label'] == 'Compliant']
        
        target_compliant_count = int(len(non_compliant) * target_ratio / (1 - target_ratio))
        needed_compliant = max(0, target_compliant_count - len(compliant))
        
        print(f"Creating {needed_compliant} compliant samples for balance...")
        
        new_compliant = []
        for _ in range(needed_compliant):
            # Take a non-compliant sample and make it compliant
            base_sample = random.choice(non_compliant)
            compliant_variant = copy.deepcopy(base_sample)
            
            # Update to compliant
            compliant_variant['case_id'] = f"AUG-{uuid.uuid4().hex[:8]}"
            compliant_variant['timestamp'] = datetime.now().isoformat()
            compliant_variant['original_prediction'] = 'Non-Compliant'
            compliant_variant['corrected_label'] = 'Compliant'
            
            # Create compliant reasoning
            reg_type = compliant_variant['feature_characteristics']['regulation_type']
            geo = compliant_variant['feature_characteristics']['geographic']
            jurisdiction = geo.get('country', geo.get('region', 'jurisdiction'))
            
            compliant_reasoning = [
                f"Feature properly implements {reg_type} requirements for {jurisdiction}",
                f"Adequate compliance measures in place for {reg_type} regulations",
                f"Feature meets all {jurisdiction} {reg_type} standards",
                f"Proper {reg_type} safeguards implemented according to local laws",
                f"Compliant implementation of {reg_type} requirements"
            ]
            
            compliant_variant['reviewer_reasoning'] = random.choice(compliant_reasoning)
            compliant_variant['confidence_score'] = round(random.uniform(0.8, 0.95), 2)
            compliant_variant['impact_score'] = round(random.uniform(0.3, 0.6), 2)
            
            new_compliant.append(compliant_variant)
        
        return new_compliant
    
    def augment_dataset(self, data: List[Dict], target_size: int = 200) -> List[Dict]:
        """Perform comprehensive dataset augmentation."""
        print("🔄 Starting data augmentation...")
        
        # Start with original data
        augmented_data = copy.deepcopy(data)
        
        # 1. Balance compliant/non-compliant ratio
        balanced_compliant = self.balance_compliant_samples(data)
        augmented_data.extend(balanced_compliant)
        
        print(f"✅ Added {len(balanced_compliant)} balanced compliant samples")
        
        # 2. Geographic expansion
        geographic_variants = []
        for original in data:
            current_geo = original['feature_characteristics']['geographic']
            current_country = current_geo.get('country')
            
            if current_country in self.jurisdiction_mappings:
                # Create variants for similar jurisdictions
                mapping = self.jurisdiction_mappings[current_country]
                
                if current_country == 'USA':
                    # Create state variants
                    for _ in range(2):  # 2 variants per original
                        variant = self.create_geographic_variant(original, 'USA')
                        geographic_variants.append(variant)
                else:
                    # Create country variants
                    for similar_country in mapping['similar_countries'][:2]:
                        variant = self.create_geographic_variant(original, similar_country)
                        geographic_variants.append(variant)
        
        augmented_data.extend(geographic_variants)
        print(f"✅ Added {len(geographic_variants)} geographic variants")
        
        # 3. Temporal variations
        temporal_variants = []
        for original in data:
            # Create 1-2 temporal variants per original
            for _ in range(random.randint(1, 2)):
                variant = self.create_temporal_variant(original)
                temporal_variants.append(variant)
        
        augmented_data.extend(temporal_variants)
        print(f"✅ Added {len(temporal_variants)} temporal variants")
        
        # 4. Regulation type cross-pollination
        regulation_variants = []
        regulation_types = list(self.regulation_patterns.keys())
        
        for original in data:
            current_reg = original['feature_characteristics']['regulation_type']
            
            # Create variants with related regulation types
            related_regs = [reg for reg in regulation_types if reg != current_reg]
            for target_reg in random.sample(related_regs, min(2, len(related_regs))):
                variant = self.create_regulation_variant(original, target_reg)
                regulation_variants.append(variant)
        
        augmented_data.extend(regulation_variants)
        print(f"✅ Added {len(regulation_variants)} regulation variants")
        
        # 5. Trim to target size if needed
        if len(augmented_data) > target_size:
            # Keep all original data, sample from augmented
            original_ids = {item['case_id'] for item in data}
            original_data = [item for item in augmented_data if item['case_id'] in original_ids]
            augmented_only = [item for item in augmented_data if item['case_id'] not in original_ids]
            
            sample_size = target_size - len(original_data)
            sampled_augmented = random.sample(augmented_only, min(sample_size, len(augmented_only)))
            
            augmented_data = original_data + sampled_augmented
        
        print(f"🎯 Final dataset size: {len(augmented_data)}")
        return augmented_data
    
    def save_augmented_data(self, data: List[Dict], filepath: str):
        """Save augmented dataset."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved augmented dataset to {filepath}")
    
    def generate_augmentation_report(self, original_data: List[Dict], augmented_data: List[Dict]) -> str:
        """Generate detailed augmentation report."""
        original_analysis = self.analyze_dataset(original_data)
        augmented_analysis = self.analyze_dataset(augmented_data)
        
        report = f"""# Data Augmentation Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Original Dataset Analysis
- **Total Records**: {original_analysis['total_records']}
- **Label Distribution**: {dict(original_analysis['label_distribution'])}
- **Regulation Types**: {dict(original_analysis['regulation_distribution'])}
- **Geographic Distribution**: {dict(original_analysis['geographic_distribution'])}

## Augmented Dataset Analysis
- **Total Records**: {augmented_analysis['total_records']} (+{augmented_analysis['total_records'] - original_analysis['total_records']})
- **Label Distribution**: {dict(augmented_analysis['label_distribution'])}
- **Regulation Types**: {dict(augmented_analysis['regulation_distribution'])}
- **Geographic Distribution**: {dict(augmented_analysis['geographic_distribution'])}

## Augmentation Strategies Applied
1. **Class Balancing**: Generated compliant samples to improve label balance
2. **Geographic Expansion**: Created variants for similar jurisdictions
3. **Temporal Variations**: Generated time-shifted variants with realistic changes
4. **Regulation Cross-pollination**: Adapted samples across related regulation types

## Quality Measures
- Maintained legal terminology accuracy
- Preserved jurisdiction-specific compliance patterns
- Ensured realistic confidence score distributions
- Generated diverse feature type coverage

## Impact Analysis
- **Size Increase**: {((augmented_analysis['total_records'] / original_analysis['total_records']) - 1) * 100:.1f}%
- **Balance Improvement**: Compliant ratio improved from {original_analysis['label_distribution']['Compliant'] / original_analysis['total_records']:.1%} to {augmented_analysis['label_distribution']['Compliant'] / augmented_analysis['total_records']:.1%}
- **Geographic Diversity**: Expanded from {len(original_analysis['geographic_distribution'])} to {len(augmented_analysis['geographic_distribution'])} jurisdictions
- **Regulation Coverage**: Maintained {len(augmented_analysis['regulation_distribution'])} regulation types
"""
        
        return report

def main():
    """Main augmentation pipeline."""
    print("🚀 Geo-Compliance Data Augmentation Pipeline")
    print("=" * 60)
    
    # Initialize augmenter
    augmenter = ComplianceDataAugmenter()
    
    # Load original data
    original_data = augmenter.load_data('active_learning_data/corrections.json')
    print(f"📥 Loaded {len(original_data)} original records")
    
    # Analyze original dataset
    analysis = augmenter.analyze_dataset(original_data)
    print(f"📊 Original dataset analysis:")
    print(f"   • Labels: {dict(analysis['label_distribution'])}")
    print(f"   • Regulations: {dict(analysis['regulation_distribution'])}")
    print(f"   • Geography: {dict(analysis['geographic_distribution'])}")
    
    # Perform augmentation
    target_size = 150  # Reasonable target for small dataset
    augmented_data = augmenter.augment_dataset(original_data, target_size)
    
    # Save augmented dataset
    augmenter.save_augmented_data(augmented_data, 'active_learning_data/corrections_augmented.json')
    
    # Generate and save report
    report = augmenter.generate_augmentation_report(original_data, augmented_data)
    with open('active_learning_data/augmentation_report.md', 'w') as f:
        f.write(report)
    
    print("✅ Augmentation completed successfully!")
    print(f"📈 Dataset expanded from {len(original_data)} to {len(augmented_data)} records")
    print("📄 Report saved to: active_learning_data/augmentation_report.md")
    
    return augmented_data

if __name__ == "__main__":
    main()
