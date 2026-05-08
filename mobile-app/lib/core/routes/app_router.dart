import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'routes.dart';
import 'src/splash_route.dart';

final GlobalKey<NavigatorState> rootNavigatorKey = GlobalKey<NavigatorState>();

final GoRouter appRouter = GoRouter(
  initialLocation: Routes.splash.path,
  navigatorKey: rootNavigatorKey,
  routes: [splashRoute],
  // observers: [HeroineController()],
  debugLogDiagnostics: true,
  onException: (context, state, exception) {
    Routes.splash.go(context);
  },
);
