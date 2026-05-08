import 'package:flutter/material.dart';
import 'package:starlight/shared/helpers/extensions/extensions.dart';

class AnimatedSizing extends StatelessWidget {
  final Duration? duration;
  final Curve? curve;
  final Widget child;
  const AnimatedSizing({super.key, this.duration, this.curve, required this.child});
  factory AnimatedSizing.fast({required Widget child}) {
    return AnimatedSizing(duration: 400.inMs, child: child);
  }

  factory AnimatedSizing.normal({required Widget child}) {
    return AnimatedSizing(child: child);
  }

  factory AnimatedSizing.slow({required Widget child}) {
    return AnimatedSizing(duration: 1000.inMs, child: child);
  }
  @override
  Widget build(BuildContext context) =>
      AnimatedSize(duration: duration ?? 700.inMs, curve: curve ?? Curves.decelerate, child: child);
}
