import 'dart:ui';

import 'package:starlight/shared/components/layout/app_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:starlight/shared/helpers/extensions/extensions.dart';

class AppBarContainerChild extends ConsumerWidget {
  const AppBarContainerChild(
    this.isDarkMode, {
    super.key,
    required this.title,
    this.titleStyle,
    this.subtitle,
    this.subtitleStyle,
    this.tooltipMessage,
    this.onBackButtonClicked,
    this.titleWidget,
    this.trailing,
    this.padding,
  });

  final bool isDarkMode;
  final String title;
  final String? subtitle;
  final TextStyle? titleStyle;
  final TextStyle? subtitleStyle;
  final String? tooltipMessage;
  final void Function()? onBackButtonClicked;
  final Widget? titleWidget;
  final Widget? trailing;
  final EdgeInsets? padding;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = context.theme;
    return Tooltip(
      triggerMode: TooltipTriggerMode.tap,
      message: tooltipMessage ?? title,
      showDuration: 4.inSeconds,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: Row(
          children: [
            AppBackButton(onPressed: onBackButtonClicked),
            8.inRow,
            Expanded(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Flexible(
                    child: Container(
                      constraints: BoxConstraints(maxHeight: kToolbarHeight),
                      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.surface.withValues(alpha: 0.25),
                        border: Border.fromBorderSide(
                          BorderSide(color: theme.colorScheme.onSurface.withValues(alpha: 0.04)),
                        ),
                        borderRadius: BorderRadius.circular(40),
                      ),
                      child:
                          titleWidget ??
                          ((subtitle != null || (subtitle != null && subtitle!.isNotEmpty))
                              ? Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  // spacing: 0,
                                  children: [
                                    Expanded(
                                      child: AppText(
                                        title,
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        overflow: TextOverflow.ellipsis,
                                        maxLines: 1,
                                      ),
                                    ),
                                    AppText(
                                      subtitle!,
                                      fontSize: 12,
                                      overflow: TextOverflow.ellipsis,
                                      style: subtitleStyle,
                                      maxLines: 1,
                                    ),
                                  ],
                                )
                              : AppText(
                                  title,
                                  fontSize: 17,
                                  fontWeight: FontWeight.bold,
                                  overflow: TextOverflow.ellipsis,
                                  style: titleStyle,
                                  maxLines: 2,
                                )),
                    ),
                  ),
                ],
              ),
            ),
            8.inRow,
            ?trailing,
          ],
        ),
      ),
    );
  }
}

class AppBackButton extends ConsumerWidget {
  final Color? backgroundColor;
  final void Function()? onPressed;
  const AppBackButton({super.key, this.backgroundColor, this.onPressed});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = context.theme;
    return ClipOval(
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 2, sigmaY: 2),
        child: ElevatedButton(
          onPressed: () {
            if (onPressed == null) {
              context.pop();
              return;
            } else {
              onPressed!();
            }
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: theme.scaffoldBackgroundColor.withValues(alpha: 0.6),
            fixedSize: const Size(40, 40),
            padding: EdgeInsets.zero,
            shape: CircleBorder(side: BorderSide(color: theme.colorScheme.outline.withValues(alpha: .1))),
          ),
          child: Icon(Icons.arrow_back_ios_new_rounded, size: 20, color: theme.iconTheme.color),
        ),
      ),
    );
    // return IconButton(
    //   color: theme.supportingText,
    //   onPressed: () {
    //     if (onPressed == null) {
    //       context.pop();
    //       return;
    //     } else {
    //       onPressed!();
    //     }
    //   },
    //   icon: Icon(Icons.arrow_back_ios_new_rounded, size: 20, color: theme.supportingText),
    //   style: ButtonStyle(
    //     backgroundColor: WidgetStatePropertyAll(backgroundColor ?? theme.altBackgroundPrimary.withValues(alpha: 0.9)),
    //     shape: WidgetStatePropertyAll(CircleBorder(side: BorderSide(color: ref.onBackground.withAlpha(10)))),
    //   ),
    // );
  }
}
