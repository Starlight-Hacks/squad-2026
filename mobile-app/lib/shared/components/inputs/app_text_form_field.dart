import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:starlight/shared/components/layout/app_text.dart';
import 'package:starlight/shared/theme/colors.dart';

/// A styled text form field matching the starlight Figma design system.
///
/// Dark variant: [AppColors.backgroundSurface] fill, [AppColors.borderDefault]
/// border, 6px radius, 48px height, [AppColors.textMuted] hint.
/// Focused border switches to [AppColors.primary].
class AppTextFormField extends StatelessWidget {
  final String? titleText;
  final Widget? title;
  final TextStyle? titleStyle;
  final Widget? footer;

  final double? height;
  final TextInputType? keyboardType;
  final bool readOnly;
  final String obscuringCharacter;
  final bool obscureText;
  final void Function()? onEditingComplete;
  final void Function(String)? onFieldSubmitted;
  final void Function(String?)? onSaved;
  final void Function(String)? onChanged;
  final void Function()? onTap;
  final void Function(PointerDownEvent)? onTapOutside;
  final String? Function(String?)? validator;
  final List<TextInputFormatter>? inputFormatters;
  final String? initialValue;
  final String? hintText;
  final String? errorText;
  final Widget? error;
  final TextStyle? errorStyle;
  final EdgeInsets? contentPadding;
  final Widget? prefix;
  final Widget? prefixIcon;
  final Widget? suffix;
  final bool enabled;
  final TextEditingController? controller;
  final TextInputAction? textInputAction;
  final Iterable<String>? autofillHints;
  final bool autofocus;
  final bool autocorrect;
  final AutovalidateMode? autovalidateMode;
  final Color? fillColor;
  final Color? borderColor;
  final int? minLines;
  final int? maxLines;
  final int? maxLength;
  final FocusNode? focusNode;

  const AppTextFormField({
    super.key,
    this.titleText,
    this.title,
    this.titleStyle,
    this.footer,
    this.height,
    this.keyboardType,
    this.readOnly = false,
    this.obscuringCharacter = '•',
    this.obscureText = false,
    this.onEditingComplete,
    this.onFieldSubmitted,
    this.onSaved,
    this.onChanged,
    this.onTap,
    this.onTapOutside,
    this.validator,
    this.inputFormatters,
    this.initialValue,
    this.hintText,
    this.errorText,
    this.error,
    this.errorStyle,
    this.contentPadding,
    this.prefix,
    this.prefixIcon,
    this.suffix,
    this.enabled = true,
    this.controller,
    this.textInputAction,
    this.autofillHints,
    this.autofocus = false,
    this.autocorrect = true,
    this.autovalidateMode,
    this.fillColor,
    this.borderColor,
    this.minLines,
    this.maxLines = 1,
    this.maxLength,
    this.focusNode,
  });

  @override
  Widget build(BuildContext context) {
    final hasWrapper = titleText != null || title != null || footer != null;
    final field = _starlightTextFormField(data: this);

    if (!hasWrapper) {
      return SizedBox(height: height, width: double.infinity, child: field);
    }

    return SizedBox(
      height: height,
      width: double.infinity,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: 6,
        children: [
          if (title != null)
            title!
          else if (titleText != null)
            AppText(titleText!, fontSize: 12, fontWeight: FontWeight.w500, color: AppColors.textSecondary),
          field,
          if (footer != null) footer!,
        ],
      ),
    );
  }
}

class _starlightTextFormField extends StatelessWidget {
  final AppTextFormField data;
  const _starlightTextFormField({required this.data});

  @override
  Widget build(BuildContext context) {
    final d = data;
    return TextFormField(
      enabled: d.enabled,
      controller: d.controller,
      focusNode: d.focusNode,
      onTapOutside: d.onTapOutside,
      keyboardType: d.keyboardType,
      readOnly: d.readOnly,
      obscuringCharacter: d.obscuringCharacter,
      obscureText: d.obscureText,
      onEditingComplete: d.onEditingComplete,
      onFieldSubmitted: d.onFieldSubmitted,
      onSaved: d.onSaved,
      validator: d.validator,
      inputFormatters: d.inputFormatters,
      initialValue: d.initialValue,
      onChanged: d.onChanged,
      onTap: d.onTap,
      minLines: d.minLines,
      maxLines: d.maxLines,
      maxLength: d.maxLength,
      textInputAction: d.textInputAction,
      autofillHints: d.autofillHints,
      autocorrect: d.autocorrect,
      autofocus: d.autofocus,
      autovalidateMode: d.autovalidateMode,
      style: const TextStyle(
        fontFamily: 'Geist',
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: AppColors.textPrimary,
        height: 1.29,
      ),
      cursorColor: AppColors.primary,
      cursorRadius: const Radius.circular(2),
      decoration: InputDecoration(
        filled: true,
        fillColor: d.fillColor ?? AppColors.backgroundSurface,
        hintText: d.hintText,
        hintStyle: const TextStyle(
          fontFamily: 'Geist',
          fontSize: 14,
          fontWeight: FontWeight.w400,
          color: AppColors.textMuted,
          height: 1.29,
        ),
        errorText: d.errorText,
        error: d.error,
        errorStyle: d.errorStyle ?? const TextStyle(fontFamily: 'Geist', fontSize: 12, color: Color(0xFFEF4444)),
        contentPadding: d.contentPadding ?? const EdgeInsets.symmetric(horizontal: 12, vertical: 15),
        prefix: d.prefix,
        prefixIcon: d.prefixIcon,
        suffixIcon: d.suffix,
        border: _border(d.borderColor ?? AppColors.borderDefault),
        enabledBorder: _border(d.borderColor ?? AppColors.borderDefault),
        focusedBorder: _border(AppColors.primary),
        focusedErrorBorder: _border(const Color(0xFFEF4444)),
        errorBorder: _border(const Color(0xFFEF4444)),
        disabledBorder: _border(AppColors.borderDefault.withValues(alpha: 0.4)),
      ),
    );
  }

  OutlineInputBorder _border(Color color) => OutlineInputBorder(
    borderSide: BorderSide(color: color),
    borderRadius: BorderRadius.circular(6),
  );
}
