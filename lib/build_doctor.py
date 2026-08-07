import os
import re
from pathlib import Path

def diagnose_android_build(project_path="."):
    """
    Analyzes Android Gradle configuration for common issues, 16KB alignment, and dependencies.
    """
    root = Path(project_path).resolve()
    issues = []
    recommendations = []

    build_gradle = root / "build.gradle"
    app_build_gradle = root / "app" / "build.gradle"
    settings_gradle = root / "settings.gradle"

    if not app_build_gradle.exists():
        return {"is_android": False, "issues": ["No app/build.gradle found"], "recommendations": []}

    try:
        with open(app_build_gradle, "r", encoding="utf-8", errors="ignore") as f:
            app_content = f.read()

        # Check compileSdk / targetSdk
        sdk_match = re.search(r'targetSdk(?:Version)?\s+(\d+)', app_content)
        if sdk_match:
            target_sdk = int(sdk_match.group(1))
            if target_sdk < 34:
                issues.append(f"Target SDK is {target_sdk} (< 34). Android 14+ requires targetSdk >= 34.")
                recommendations.append("Update targetSdk and compileSdk to 34 in app/build.gradle")
        
        # Check Compose compiler version
        if "compose true" in app_content or "compose = true" in app_content:
            if "kotlinCompilerExtensionVersion" not in app_content:
                issues.append("Compose is enabled but kotlinCompilerExtensionVersion is not explicitly declared.")
                recommendations.append("Add composeOptions { kotlinCompilerExtensionVersion '1.5.8' }")

        # Check 16KB page-alignment native flags (piuu native core requirement)
        if "ndk" in app_content or "externalNativeBuild" in app_content:
            if "-Wl,-z,max-page-size=16384" not in app_content and "16384" not in app_content:
                issues.append("Native C/C++ build detected without explicit 16KB page-alignment linker flags.")
                recommendations.append("Add ldLibs '-Wl,-z,max-page-size=16384' in cmake/ndk config.")

    except Exception as e:
        issues.append(f"Failed to read app/build.gradle: {e}")

    return {
        "is_android": True,
        "issues": issues,
        "recommendations": recommendations,
        "healthy": len(issues) == 0
    }

def auto_fix_build_issues(project_path="."):
    """
    Applies non-destructive automatic fixes for common configuration issues.
    """
    root = Path(project_path).resolve()
    fixes_applied = []
    
    # 1. Fix shebangs on gradle wrappers and scripts
    for item in [root / "gradlew", root / "scripts"]:
        if item.exists():
            from env_checker import batch_fix_shebangs
            fixed = batch_fix_shebangs(item if item.is_dir() else item.parent)
            if fixed:
                fixes_applied.extend(fixed)

    return fixes_applied
