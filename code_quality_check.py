#!/usr/bin/env python3
"""Code Quality Assessment"""

import os
import ast
import re

def check_file_quality(filepath):
    """Check code quality metrics for a Python file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    warnings = []
    
    # Check 1: File has docstring
    if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
        issues.append("Missing module docstring")
    
    # Check 2: Imports organization
    lines = content.split('\n')
    import_section = []
    for i, line in enumerate(lines[:50]):  # Check first 50 lines
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            import_section.append((i, line))
    
    # Check 3: Function/class documentation
    try:
        tree = ast.parse(content)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        undocumented_functions = []
        for func in functions:
            if not ast.get_docstring(func):
                undocumented_functions.append(func.name)
        
        undocumented_classes = []
        for cls in classes:
            if not ast.get_docstring(cls):
                undocumented_classes.append(cls.name)
        
        if undocumented_functions:
            warnings.append(f"Undocumented functions: {', '.join(undocumented_functions[:5])}")
        if undocumented_classes:
            warnings.append(f"Undocumented classes: {', '.join(undocumented_classes)}")
    except:
        pass
    
    # Check 4: Line length (PEP 8: max 79-100 chars)
    long_lines = []
    for i, line in enumerate(lines, 1):
        if len(line) > 120:  # Being lenient
            long_lines.append(i)
    
    if len(long_lines) > 10:
        warnings.append(f"Many long lines (>120 chars): {len(long_lines)} lines")
    
    # Check 5: Error handling
    has_try_except = 'try:' in content and 'except' in content
    if not has_try_except:
        warnings.append("No error handling (try/except) found")
    
    # Check 6: Logging
    has_logging = 'logger' in content or 'logging' in content or 'print(' in content
    if not has_logging:
        warnings.append("No logging/debugging output")
    
    # Check 7: Type hints
    has_type_hints = '-> ' in content or ': str' in content or ': int' in content
    if not has_type_hints:
        warnings.append("No type hints found")
    
    return {
        'issues': issues,
        'warnings': warnings,
        'lines': len(lines),
        'functions': len(functions) if 'functions' in locals() else 0,
        'classes': len(classes) if 'classes' in locals() else 0
    }

def check_project_structure():
    """Check overall project structure"""
    
    required_files = [
        'README.md',
        'requirements.txt',
        '.env.example',
        '.gitignore'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    return missing

def main():
    print("="*80)
    print("CODE QUALITY ASSESSMENT")
    print("="*80)
    
    # Check project structure
    print("\n1. PROJECT STRUCTURE")
    print("-" * 80)
    missing = check_project_structure()
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
    else:
        print("✅ All required files present")
    
    # Check if documentation exists
    docs = ['README.md', 'ARCHITECTURE.md']
    existing_docs = [d for d in docs if os.path.exists(d)]
    print(f"✅ Documentation: {', '.join(existing_docs)}")
    
    # Check Python files
    print("\n2. PYTHON CODE QUALITY")
    print("-" * 80)
    
    python_files = [
        'main.py',
        'enhanced_extractor.py',
        'enhanced_response.py',
        'red_flag_detector.py'
    ]
    
    total_issues = 0
    total_warnings = 0
    
    for filepath in python_files:
        if not os.path.exists(filepath):
            print(f"\n❌ {filepath}: NOT FOUND")
            continue
        
        result = check_file_quality(filepath)
        
        status = "✅" if not result['issues'] else "❌"
        print(f"\n{status} {filepath}")
        print(f"   Lines: {result['lines']} | Functions: {result['functions']} | Classes: {result['classes']}")
        
        if result['issues']:
            total_issues += len(result['issues'])
            for issue in result['issues']:
                print(f"   ❌ ISSUE: {issue}")
        
        if result['warnings']:
            total_warnings += len(result['warnings'])
            for warning in result['warnings'][:3]:  # Show top 3
                print(f"   ⚠️  WARNING: {warning}")
    
    # Overall score
    print("\n" + "="*80)
    print("OVERALL ASSESSMENT")
    print("="*80)
    
    score = 100
    score -= total_issues * 10  # -10 per critical issue
    score -= total_warnings * 2  # -2 per warning
    score = max(0, score)
    
    print(f"\nCritical Issues: {total_issues}")
    print(f"Warnings: {total_warnings}")
    print(f"\nEstimated Code Quality Score: {score}/100")
    
    if score >= 90:
        print("🎉 EXCELLENT - Production ready!")
    elif score >= 75:
        print("✅ GOOD - Minor improvements recommended")
    elif score >= 60:
        print("👍 ACCEPTABLE - Some improvements needed")
    else:
        print("⚠️  NEEDS WORK - Significant improvements required")
    
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    print("1. ✅ Add docstrings to all functions and classes")
    print("2. ✅ Add type hints for better code clarity")
    print("3. ✅ Add comprehensive error handling")
    print("4. ✅ Keep lines under 100 characters")
    print("5. ✅ Add logging for debugging")
    print("6. ✅ Write unit tests (test_*.py files)")
    print("7. ✅ Add CI/CD configuration (.github/workflows)")
    print("8. ✅ Make repository PUBLIC on GitHub")

if __name__ == "__main__":
    main()
