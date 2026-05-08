import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

enum Routes {
  /// Splash Screen
  splash,
}

extension RoutesExtension on Routes {
  String get path => name.withSlashPrefix;
  String get subPath => name;
  void go(BuildContext context) => context.goNamed(name);
  void push(BuildContext context) => context.pushNamed(name);
}

extension RoutesHelper on String {
  String get lastRoutePath => substring(lastIndexOf('/') + 1);
  String get withSlashPrefix => startsWith('/') ? this : '/$this';
}
