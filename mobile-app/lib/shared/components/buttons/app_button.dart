import 'package:starlight/shared/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:starlight/shared/components/layout/app_text.dart';

enum ButtonType { filled, outlined }

class AppButton extends StatelessWidget {
  /// Type can be [ButtonType.filled] or [ButtonType.outlined]
  final ButtonType type;

  /// Used for Semantics if [child] is provided
  final String label;

  /// These can be of type [Flexible], [Expanded] or [Widget] since they are placed in a Row internally
  final Widget? leading;
  final Widget? trailing;

  final double? labelSize;
  final Color? labelColor;

  /// Default Color -> [AppColors.primaryColorB600]
  final Color? color;
  final VoidCallback? onPressed;
  final VoidCallback? onLongPress;

  final double borderRadius;
  final Size? size;
  final EdgeInsets? padding;

  /// For Implicit Styling(Other properties like color will be ignored if provided)
  final ButtonStyle? style;
  final bool isLoading;

  final double? outlinedBorderWidth;
  final Color? overlayColor;

  /// [label], [leading] and [trailing] will be ignored if child is provided.
  final Widget? child;
  const AppButton({
    super.key,
    required this.label,
    this.leading,
    this.trailing,
    this.type = ButtonType.filled,
    this.color,
    this.borderRadius = 6,
    this.size,
    this.style,
    this.padding,
    required this.onPressed,
    this.onLongPress,
    this.child,
    this.labelSize,
    this.labelColor,
    this.isLoading = false,
    this.outlinedBorderWidth,
    this.overlayColor,
  });

  Widget _defaultChild([Color? color]) => FittedBox(
    child: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      spacing: 8,
      children: [
        leading ?? const SizedBox.shrink(),
        AppText(
          label,
          fontSize: labelSize ?? 14,
          color: color ?? labelColor?.withValues(alpha: onPressed == null ? 0.4 : 1) ?? AppColors.black,
          fontWeight: FontWeight.w600,
        ),
        trailing ?? const SizedBox.shrink(),
      ],
    ),
  );
  Widget get _buildLoadingIndicator => SizedBox.square(
    dimension: 20,
    child: CircularProgressIndicator(strokeCap: StrokeCap.round, color: labelColor),
  );

  @override
  Widget build(BuildContext context) {
    return switch (type) {
      ButtonType.filled => ElevatedButton(
        onPressed: onPressed,
        onLongPress: onLongPress,
        style:
            style ??
            ElevatedButton.styleFrom(
              disabledBackgroundColor: AppColors.battleshipGrey,
              backgroundColor: color ?? AppColors.white,
              splashFactory: InkSparkle.splashFactory,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(borderRadius)),
              // fixedSize: size ?? Size.fromHeight(50),
              fixedSize: size ?? const Size.fromHeight(50),
              padding: padding,
              elevation: 0.0,
            ),
        child: isLoading ? _buildLoadingIndicator : (child ?? _defaultChild()),
      ),
      ButtonType.outlined => OutlinedButton(
        onPressed: onPressed,
        style:
            style ??
            OutlinedButton.styleFrom(
              side: BorderSide(color: color ?? AppColors.primaryDark, width: outlinedBorderWidth ?? 1.0),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(borderRadius),
                side: BorderSide(color: color ?? AppColors.primaryDark),
              ),
              fixedSize: size ?? const Size.fromHeight(50),
              padding: padding,
              elevation: 0.0,
            ),
        child: isLoading ? _buildLoadingIndicator : (child ?? _defaultChild(color ?? AppColors.primaryDark)),
      ),
    };
  }
}
