import 'package:flutter/material.dart';
import 'package:starlight/shared/theme/colors.dart';
import 'package:google_fonts/google_fonts.dart';

class Themes {
  Themes._();

  static final ThemeData lightTheme = ThemeData(
    brightness: Brightness.light,
    primaryColor: AppColors.primary,
    scaffoldBackgroundColor: AppColors.white,
    fontFamily: 'Geist',
    splashFactory: InkSparkle.splashFactory,
    splashColor: Colors.transparent,
    highlightColor: Colors.transparent,
    colorScheme: const ColorScheme.light(
      primary: AppColors.primary,
      surface: AppColors.white,
      onPrimary: AppColors.white,
      onSurface: AppColors.black,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.white,
      foregroundColor: AppColors.black,
      elevation: 0,
      scrolledUnderElevation: 0,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: AppColors.black,
      foregroundColor: AppColors.white,
      elevation: 0,
    ),
    textTheme: _buildTextTheme(AppColors.black),
    inputDecorationTheme: _buildInputDecorationTheme(
      fillColor: const Color(0xFFF9FAFB),
      borderColor: const Color(0xFFD1D5DB),
      focusedBorderColor: AppColors.primary,
      hintColor: AppColors.textMuted,
    ),
    dividerColor: const Color(0xFFE5E7EB),
    cardColor: AppColors.white,
  );

  static final ThemeData darkTheme = ThemeData(
    brightness: Brightness.dark,
    primaryColor: AppColors.primary,
    scaffoldBackgroundColor: AppColors.backgroundBase,
    fontFamily: 'Geist',
    splashFactory: InkSparkle.splashFactory,
    splashColor: Colors.transparent,
    highlightColor: Colors.transparent,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.primary,
      surface: AppColors.backgroundSurface,
      onPrimary: AppColors.white,
      onSurface: AppColors.textPrimary,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.backgroundBase,
      foregroundColor: AppColors.textPrimary,
      elevation: 0,
      scrolledUnderElevation: 0,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: AppColors.white,
      foregroundColor: AppColors.black,
      elevation: 0,
    ),
    textTheme: _buildTextTheme(AppColors.textPrimary),
    inputDecorationTheme: _buildInputDecorationTheme(
      fillColor: AppColors.backgroundSurface,
      borderColor: AppColors.borderDefault,
      focusedBorderColor: AppColors.primary,
      hintColor: AppColors.textMuted,
    ),
    dividerColor: AppColors.borderSubtle,
    cardColor: AppColors.backgroundSurface,
  );

  // ============================================================
  // Shared text theme builder
  // ============================================================

  /// Builds a [TextTheme] using Geist with sensible defaults.
  static TextTheme _buildTextTheme(Color defaultColor) {
    return GoogleFonts.geistTextTheme(
      TextTheme(
        // Headings
        headlineLarge: TextStyle(
          fontFamily: 'Geist',
          fontSize: 24,
          fontWeight: FontWeight.w700,
          color: defaultColor,
          height: 1.33,
        ),
        headlineMedium: TextStyle(
          fontFamily: 'Geist',
          fontSize: 18,
          fontWeight: FontWeight.w700,
          color: defaultColor,
          height: 1.56,
        ),
        headlineSmall: TextStyle(
          fontFamily: 'Geist',
          fontSize: 16,
          fontWeight: FontWeight.w700,
          color: defaultColor,
          height: 1.5,
        ),

        // Titles
        titleLarge: TextStyle(
          fontFamily: 'Geist',
          fontSize: 16,
          fontWeight: FontWeight.w500,
          color: defaultColor,
          height: 1.5,
        ),
        titleMedium: TextStyle(
          fontFamily: 'Geist',
          fontSize: 14,
          fontWeight: FontWeight.w500,
          color: defaultColor,
          height: 1.43,
        ),
        titleSmall: TextStyle(
          fontFamily: 'Geist',
          fontSize: 12,
          fontWeight: FontWeight.w500,
          color: defaultColor,
          height: 1.33,
        ),

        // Body
        bodyLarge: TextStyle(
          fontFamily: 'Geist',
          fontSize: 14,
          fontWeight: FontWeight.w400,
          color: defaultColor,
          height: 1.43,
        ),
        bodyMedium: TextStyle(
          fontFamily: 'Geist',
          fontSize: 12,
          fontWeight: FontWeight.w400,
          color: defaultColor,
          height: 1.33,
        ),
        bodySmall: TextStyle(
          fontFamily: 'Geist',
          fontSize: 10,
          fontWeight: FontWeight.w400,
          color: defaultColor,
          height: 1.5,
        ),

        // Labels
        labelLarge: TextStyle(
          fontFamily: 'Geist',
          fontSize: 14,
          fontWeight: FontWeight.w500,
          color: defaultColor,
          height: 1.43,
        ),
        labelMedium: TextStyle(
          fontFamily: 'Geist',
          fontSize: 12,
          fontWeight: FontWeight.w400,
          color: defaultColor,
          height: 1.33,
        ),
        labelSmall: TextStyle(
          fontFamily: 'Geist',
          fontSize: 10,
          fontWeight: FontWeight.w400,
          color: defaultColor,
          height: 1.5,
        ),
      ),
    );
  }

  // ============================================================
  // Shared input decoration theme builder
  // ============================================================

  /// Builds a consistent [InputDecorationTheme] from Figma tokens.
  static InputDecorationTheme _buildInputDecorationTheme({
    required Color fillColor,
    required Color borderColor,
    required Color focusedBorderColor,
    required Color hintColor,
  }) {
    const radius = BorderRadius.all(Radius.circular(6));
    return InputDecorationTheme(
      filled: true,
      fillColor: fillColor,
      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
      hintStyle: TextStyle(
        fontFamily: 'Geist',
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: hintColor,
        height: 1.29,
      ),
      border: OutlineInputBorder(
        borderRadius: radius,
        borderSide: BorderSide(color: borderColor),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: radius,
        borderSide: BorderSide(color: borderColor),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: radius,
        borderSide: BorderSide(color: focusedBorderColor),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: radius,
        borderSide: const BorderSide(color: Color(0xFFEF4444)),
      ),
      focusedErrorBorder: OutlineInputBorder(
        borderRadius: radius,
        borderSide: const BorderSide(color: Color(0xFFEF4444)),
      ),
      disabledBorder: OutlineInputBorder(
        borderRadius: radius,
        borderSide: BorderSide(color: borderColor.withValues(alpha: 0.4)),
      ),
    );
  }
}
