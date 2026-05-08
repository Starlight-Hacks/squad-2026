import 'package:flutter/material.dart';

/// starlight design system color tokens.
/// Dark-first palette extracted from Figma. All semantic names map directly
/// to design layer names for easy cross-referencing.
class AppColors {
  AppColors._();

  // ============================================================
  // Brand / Primary
  // ============================================================

  /// Primary action color — used for focused borders, CTAs
  static const Color primary = Color(0xFF3559A6);

  /// Lighter primary variant — used for icon backgrounds, subtle fills
  static const Color primaryLight = Color(0xFF2E5790);

  static const Color primaryDark = Color(0xFF1E3A8A);

  // ============================================================
  // Backgrounds
  // ============================================================

  /// Page / screen background
  static const Color backgroundBase = Color(0xFF000000);

  /// Card / surface background — most common container bg
  static const Color backgroundSurface = Color(0xFF111827);

  /// Elevated surface — tab indicators, input fills, secondary cards
  static const Color backgroundElevated = Color(0xFF1F2937);

  /// Active tab indicator background
  static const Color backgroundActiveTab = Color(0xFF1F2B3B);

  /// Subtle tag / badge background
  static const Color backgroundTag = Color(0xFF374151);

  /// Light surface — used on buttons that need contrast against dark bg
  static const Color backgroundLight = Color(0xFFF4F4F5);

  // ============================================================
  // Text
  // ============================================================

  /// Primary text — headings and body on dark bg
  static const Color textPrimary = Color(0xFFFFFFFF);

  /// Secondary text — subtitles, metadata, placeholders
  static const Color textSecondary = Color(0xFF9CA3AF);

  /// Muted text — hints, timestamps, inactive labels
  static const Color textMuted = Color(0xFF6B7280);

  /// Inactive tab label
  static const Color textInactive = Color(0xFF71717A);

  /// Active tab label (dark-themed active tab)
  static const Color textActiveTab = Color(0xFFC0C0CE);

  /// Completed / done tab active label
  static const Color textActiveDone = Color(0xFF09090B);

  // ============================================================
  // Borders
  // ============================================================

  /// Default border — inputs, cards
  static const Color borderDefault = Color(0xFF374151);

  /// Subtle divider
  static const Color borderSubtle = Color(0xFF1F2937);

  /// Primary accent border
  static const Color borderPrimary = Color(0xFF3559A6);

  /// Secondary accent border
  static const Color borderPrimaryLight = Color(0xFF2E5790);

  // ============================================================
  // Status / Semantic
  // ============================================================

  // Meeting badge
  static const Color badgeMeetingBg = Color(0xFF1E3A8A);
  static const Color badgeMeetingText = Color(0xFF93C5FD);

  // Document badge
  static const Color badgeDocBg = Color(0xFF14532D);
  static const Color badgeDocText = Color(0xFF86EFAC);

  // Design / purple badge
  static const Color badgeDesignBg = Color(0xFF581C87);
  static const Color badgeDesignText = Color(0xFFD8B4FE);

  // Progress bar fill
  static const Color progressFill = Color(0xFF2E5480);
  static const Color progressTrack = Color(0xFF1F2937);

  // Completed checkmark / success
  static const Color success = Color(0xFF4ADE80);

  // ============================================================
  // File type icon backgrounds
  // ============================================================

  static const Color fileDocxBg = Color(0xFF1E3A8A);
  static const Color fileDocxIcon = Color(0xFF93C5FD);

  static const Color fileXlsxBg = Color(0xFF14532D);
  static const Color fileXlsxIcon = Color(0xFF86EFAC);

  static const Color filePdfBg = Color(0xFF7F1D1D);
  static const Color filePdfIcon = Color(0xFFFCA5A5);

  // Quick access icon colors
  static const Color quickAccessReports = Color(0xFF60A5FA);
  static const Color quickAccessTemplates = Color(0xFF4ADE80);
  static const Color quickAccessPdfs = Color(0xFFF87171);
  static const Color quickAccessShared = Color(0xFFC084FC);

  // ============================================================
  // Chat / Message bubbles
  // ============================================================

  /// Outgoing message bubble
  static const Color bubbleOutgoing = Color(0xFFEAEAEA);
  static const Color bubbleOutgoingText = Color(0xFF000000);

  /// Incoming message bubble
  static const Color bubbleIncoming = Color(0xFF1F2937);
  static const Color bubbleIncomingText = Color(0xFFFFFFFF);

  // ============================================================
  // Misc
  // ============================================================

  static const Color white = Color(0xFFFFFFFF);
  static const Color black = Color(0xFF000000);
  static const Color starlightGray = Color(0xFF71717A);
  static const Color arsenic = Color(0xFF202938);
  static const Color battleshipGrey = Color(0xFF8D9598);
  static const Color darkBlue = Color(0xFF111828);
}
