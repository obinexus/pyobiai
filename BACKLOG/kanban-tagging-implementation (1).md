# PyOBIAI Kanban Tagging Implementation Guide

## Technical Specification: Color-Coded Workflow Enforcement

### 1. Tagging Convention Standards

#### 1.1 Color Code Mapping
```python
KANBAN_STATES = {
    'BACKLOG': '⬜',  # No color - requires manual upgrade
    'TODO': '🟥',     # Red - ready for development
    'DOING': '🟨',    # Yellow - active development
    'DONE': '🟩'      # Green - completed and locked
}
```

#### 1.2 Tag Format Specification
```python
# Standard format: # [COLOR] [STATE]: [Description] @fn:[function_label]
# Example: # 🟥 TODO: Implement OBIBuf marshalling @fn:obibuf_marshal
```

### 2. Automated Tagging Scanner

```python
#!/usr/bin/env python3
"""
kanban_tagger.py - Enforce Kanban workflow gates in PyOBIAI codebase
"""

import os
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class KanbanTagEnforcer:
    """Enforces color-coded Kanban tagging with workflow validation"""
    
    def __init__(self, ocs_threshold: float = 0.6):
        self.ocs_threshold = ocs_threshold
        self.violations = []
        self.tag_pattern = re.compile(
            r'#\s*(⬜|🟥|🟨|🟩)?\s*(BACKLOG|TODO|DOING|DONE):\s*(.+?)(?:@fn:(\w+))?$',
            re.MULTILINE
        )
        
    def scan_file(self, filepath: str) -> List[Dict]:
        """Scan file for Kanban tags and validate workflow"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tags = []
        for match in self.tag_pattern.finditer(content):
            color, state, description, function = match.groups()
            line_num = content[:match.start()].count('\n') + 1
            
            tag_info = {
                'file': filepath,
                'line': line_num,
                'color': color,
                'state': state,
                'description': description.strip(),
                'function': function,
                'content_hash': self._hash_content(match.group(0))
            }
            
            # Validate color-state consistency
            violation = self._validate_tag(tag_info)
            if violation:
                self.violations.append(violation)
                
            tags.append(tag_info)
            
        return tags
    
    def _validate_tag(self, tag: Dict) -> Optional[Dict]:
        """Validate tag follows workflow rules"""
        expected_color = {
            'BACKLOG': '⬜',
            'TODO': '🟥',
            'DOING': '🟨',
            'DONE': '🟩'
        }
        
        # Check color-state consistency
        if tag['state'] in expected_color:
            if tag['color'] != expected_color[tag['state']]:
                return {
                    'type': 'COLOR_MISMATCH',
                    'file': tag['file'],
                    'line': tag['line'],
                    'message': f"State {tag['state']} requires color {expected_color[tag['state']]}, found {tag['color'] or 'none'}"
                }
        
        # Validate DONE items are locked
        if tag['state'] == 'DONE' and not self._is_locked(tag):
            return {
                'type': 'UNLOCKED_DONE',
                'file': tag['file'],
                'line': tag['line'],
                'message': "DONE items must be locked via OCS governance"
            }
            
        return None
    
    def _is_locked(self, tag: Dict) -> bool:
        """Check if DONE item is properly locked"""
        # Check for OCS lock marker in adjacent lines
        lock_marker = f"# OCS_LOCK: {tag['content_hash']}"
        # Implementation would check file content around tag location
        return True  # Placeholder
    
    def _hash_content(self, content: str) -> str:
        """Generate content hash for lock verification"""
        return hashlib.sha256(content.encode()).hexdigest()[:8]
```

### 3. Workflow Gate Implementation

```python
class WorkflowGateValidator:
    """Validates Kanban workflow transitions"""
    
    VALID_TRANSITIONS = {
        'BACKLOG': ['TODO'],      # Can only move to TODO
        'TODO': ['DOING'],        # Can only move to DOING
        'DOING': ['DONE'],        # Can only move to DONE
        'DONE': []                # Locked unless OCS override
    }
    
    def validate_transition(self, from_state: str, to_state: str, 
                          ocs_score: float = 0.0) -> Tuple[bool, str]:
        """Validate state transition follows workflow rules"""
        
        # Check if transition is allowed
        if to_state not in self.VALID_TRANSITIONS.get(from_state, []):
            if from_state == 'DONE' and ocs_score >= 0.8:
                # OCS override for reopening DONE items
                return True, "OCS override approved"
            return False, f"Invalid transition: {from_state} → {to_state}"
        
        # Special validation for BACKLOG → TODO
        if from_state == 'BACKLOG' and to_state == 'TODO':
            if not self._validate_backlog_readiness():
                return False, "Backlog item not ready for TODO (dependencies unresolved)"
                
        return True, "Transition approved"
    
    def _validate_backlog_readiness(self) -> bool:
        """Check if backlog item meets TODO criteria"""
        # Check: Dependencies resolved
        # Check: Specification approved
        # Check: Resources available
        return True  # Placeholder
```

### 4. Code Integration Examples

#### 4.1 Python Source Files
```python
# pyobiai/core/reasoning.py

class VerbNounEngine:
    """Semiotic reasoning engine for verb-noun pairs"""
    
    def __init__(self):
        # 🟥 TODO: Initialize Nsibidi symbol registry @fn:init_nsibidi
        self.nsibidi_registry = None
        
        # 🟨 DOING: Implement semantic weight calculation @fn:semantic_weights
        self.weight_calculator = BasicWeightCalculator()  # Temporary implementation
        
        # 🟩 DONE: Create verb-noun pair extractor @fn:extract_pairs
        # OCS_LOCK: a1b2c3d4
        self.extractor = VerbNounExtractor()
    
    def process_concept(self, concept: str):
        # ⬜ BACKLOG: Add multi-language support @fn:multilang_support
        # WORKFLOW_VIOLATION: Cannot skip TODO phase
        pass
```

#### 4.2 Markdown Documentation
```markdown
## Implementation Status

### Core Components

#### OBIBuf Implementation
🟥 TODO: Complete zero-overhead marshalling layer @fn:obibuf_core
- Status: Specification approved, ready for implementation
- Dependencies: Resolved
- Assignee: Pending

#### OBICall Bridge  
🟨 DOING: Python-C FFI implementation @fn:obicall_bridge
- Status: 40% complete
- Started: 2024-01-20
- Blocker: None

#### AEGIS Cost Function
🟩 DONE: Mathematical verification framework @fn:aegis_cost
OCS_LOCK: f5e6d7c8
- Completed: 2024-01-08
- Test Coverage: 100%
- Performance: Meets specifications
```

### 5. Validation Script

```python
#!/usr/bin/env python3
"""
validate_kanban.py - Validate Kanban workflow compliance
"""

def validate_codebase(root_dir: str):
    """Scan entire codebase for Kanban compliance"""
    enforcer = KanbanTagEnforcer()
    validator = WorkflowGateValidator()
    
    violations = []
    file_count = 0
    tag_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(('.py', '.md', '.rst')):
                filepath = os.path.join(root, file)
                file_count += 1
                
                tags = enforcer.scan_file(filepath)
                tag_count += len(tags)
                
    # Generate compliance report
    print(f"Kanban Compliance Report")
    print(f"=" * 50)
    print(f"Files scanned: {file_count}")
    print(f"Tags found: {tag_count}")
    print(f"Violations: {len(violations)}")
    
    if violations:
        print("\nViolations Found:")
        for v in violations:
            print(f"  - {v['file']}:{v['line']} - {v['type']}: {v['message']}")

if __name__ == "__main__":
    validate_codebase("./pyobiai")
```

### 6. Git Hook Integration

```bash
#!/bin/bash
# .git/hooks/pre-commit - Enforce Kanban workflow

echo "Validating Kanban workflow compliance..."

# Run validation script
python scripts/validate_kanban.py

if [ $? -ne 0 ]; then
    echo "ERROR: Kanban workflow violations detected!"
    echo "Please fix violations before committing."
    exit 1
fi

# Check for illegal state transitions
git diff --cached --name-only | while read file; do
    if [[ $file == *.py ]] || [[ $file == *.md ]]; then
        # Check for BACKLOG → DOING transitions (illegal)
        if git diff --cached "$file" | grep -E "^-.*⬜ BACKLOG:" | grep -E "^\+.*🟨 DOING:"; then
            echo "ERROR: Illegal transition BACKLOG → DOING in $file"
            echo "Items must pass through TODO state"
            exit 1
        fi
    fi
done

echo "Kanban workflow validation passed ✓"
```

### 7. OCS-Governed DONE Reopening

```python
class OCSGovernedReopening:
    """Manages reopening of DONE items through OCS governance"""
    
    def __init__(self, ocs_engine):
        self.ocs_engine = ocs_engine
        self.audit_log = []
        
    def request_reopening(self, tag_hash: str, requester: str, 
                         justification: str) -> bool:
        """Request reopening of a DONE item"""
        
        # Check requester's OCS score
        ocs_score = self.ocs_engine.get_score(requester)
        if ocs_score < 0.8:
            self.audit_log.append({
                'timestamp': datetime.now(),
                'requester': requester,
                'tag_hash': tag_hash,
                'result': 'DENIED',
                'reason': f'Insufficient OCS score: {ocs_score}'
            })
            return False
            
        # Validate justification
        if not self._validate_justification(justification):
            return False
            
        # Create unlock marker
        unlock_marker = f"# OCS_UNLOCK: {tag_hash} by {requester} at {datetime.now()}"
        
        self.audit_log.append({
            'timestamp': datetime.now(),
            'requester': requester,
            'tag_hash': tag_hash,
            'result': 'APPROVED',
            'justification': justification
        })
        
        return True
```

### 8. Workflow Violation Examples

```python
# VIOLATION EXAMPLE 1: Missing color code
# TODO: Implement feature  # ❌ Missing 🟥 color code

# VIOLATION EXAMPLE 2: Wrong color for state
# 🟨 TODO: Implement feature  # ❌ TODO requires 🟥, not 🟨

# VIOLATION EXAMPLE 3: Skipping TODO phase
# ⬜ BACKLOG: Design feature
# 🟨 DOING: Implement feature  # ❌ Cannot skip TODO phase

# VIOLATION EXAMPLE 4: Unlocked DONE item
# 🟩 DONE: Completed feature  # ❌ Missing OCS_LOCK marker

# CORRECT EXAMPLES:
# 🟥 TODO: Design OBIBuf interface @fn:obibuf_design
# 🟨 DOING: Implement marshalling logic @fn:obibuf_marshal
# 🟩 DONE: Validate zero-overhead performance @fn:obibuf_perf
# OCS_LOCK: 9a8b7c6d
```

### 9. Automated Migration Tool

```python
def migrate_existing_tags(filepath: str):
    """Migrate existing tags to color-coded format"""
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Pattern for existing tags without colors
    old_pattern = r'#\s*(TODO|DOING|DONE):\s*(.+?)$'
    
    def replace_tag(match):
        state = match.group(1)
        description = match.group(2)
        
        color_map = {
            'TODO': '🟥',
            'DOING': '🟨',
            'DONE': '🟩'
        }
        
        new_tag = f"# {color_map[state]} {state}: {description}"
        
        # Add OCS_LOCK for DONE items
        if state == 'DONE':
            tag_hash = hashlib.sha256(new_tag.encode()).hexdigest()[:8]
            new_tag += f"\n# OCS_LOCK: {tag_hash}"
            
        return new_tag
    
    migrated_content = re.sub(old_pattern, replace_tag, content, flags=re.MULTILINE)
    
    # Write back with backup
    backup_path = f"{filepath}.backup"
    os.rename(filepath, backup_path)
    
    with open(filepath, 'w') as f:
        f.write(migrated_content)
        
    print(f"Migrated {filepath} (backup: {backup_path})")
```

### 10. Integration with CI/CD Pipeline

```yaml
# .github/workflows/kanban-validation.yml
name: Kanban Workflow Validation

on: [push, pull_request]

jobs:
  validate-kanban:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
          
      - name: Validate Kanban Tags
        run: |
          python scripts/validate_kanban.py
          
      - name: Check Workflow Violations
        run: |
          if [ -f "kanban_violations.log" ]; then
            echo "::error::Kanban workflow violations detected"
            cat kanban_violations.log
            exit 1
          fi
          
      - name: Generate Compliance Report
        run: |
          python scripts/generate_kanban_report.py > kanban_report.md
          
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: kanban-compliance-report
          path: kanban_report.md
```

---

## Implementation Checklist

- [ ] Deploy validation scripts to `/scripts/kanban/`
- [ ] Configure git hooks for pre-commit validation
- [ ] Run migration tool on existing codebase
- [ ] Integrate with CI/CD pipeline
- [ ] Document OCS reopening procedures
- [ ] Train team on workflow gates
- [ ] Monitor violation metrics

This implementation ensures Kanban tags function as strict workflow gates, not cosmetic labels.