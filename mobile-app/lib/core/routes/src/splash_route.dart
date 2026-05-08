import 'package:go_router/go_router.dart';
import 'package:starlight/features/splash.dart';
import '../routes.dart';

final splashRoute = GoRoute(
  name: Routes.splash.name,
  path: Routes.splash.path,
  builder: (context, state) => const Splash(),
);
