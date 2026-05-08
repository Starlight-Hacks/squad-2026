# Flutter Deterministic Blueprint

> A clean, scalable, highly debuggable Flutter architecture. Once you see a screen, you can predict exactly where its notifier, logic, and widgets live.

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [Widget Rules](#2-widget-rules)
3. [Code Documentation Standards](#3-code-documentation-standards)
4. [Performance Optimization](#4-performance-optimization)
5. [Folder Structure Overview](#5-folder-structure-overview)
6. [lib/core](#6-libcore)
   - [api](#61-coreapi)
   - [assets](#62-coreassets)
   - [base](#63-corebase)
   - [constants](#64-coreconstants)
   - [storage](#65-corestorage)
   - [utilities](#66-coreutilities)
   - [interop](#67-coreinterop)
   - [notifiers](#68-corenotifiers)
7. [lib/data](#7-libdata)
8. [lib/features](#8-libfeatures)
   - [ui layer](#81-ui-layer)
   - [logic layer](#82-logic-layer)
   - [providers / state layer](#83-providers--state-layer)
9. [Riverpod State Pattern](#9-riverpod-state-pattern)
10. [Shared Packages & Preferences](#10-shared-packages--preferences)

---

## 1. Core Philosophy

- Architecture is **deterministic**: given any screen name, the location of its notifier, logic, actions, and widgets is always predictable.
- Inspired by clean architecture but more **adaptable and pragmatic**.
- Unidirectional data flow: UI → Actions/Logic → Providers/Notifiers → UI.
- Every folder follows a consistent internal pattern unless it is a "title folder" (a top-level organizer with no logic of its own).
- AI tooling should check if a structural pattern already exists before inventing something new. If a pattern exists, follow it. If not, reason up a new one and apply it consistently.

---

## 2. Widget Rules

### 2.1 Keep Widgets Small and Reusable

Break large widgets into smaller, focused components. Each widget should do one thing well.

```dart
// Bad
class ComplexWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Column(
        children: [
          Text('Title'),
          TextField(),
          ElevatedButton(onPressed: () {}, child: Text('Submit')),
        ],
      ),
    );
  }
}

// Good
class TitleWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) => const Text('Title');
}

class InputWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) => const TextField();
}

class SubmitButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) =>
      ElevatedButton(onPressed: () {}, child: const Text('Submit'));
}

class ComplexWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [TitleWidget(), InputWidget(), SubmitButton()],
    );
  }
}
```

### 2.2 Widget File vs. Private Widget Decision

A widget deserves its own file if it is **reusable or significant enough** to stand alone — e.g., `ModuleListTile`, `SettingsCard`, `LibrarySearchButton`.

If a widget is only used internally within a parent widget and is **too small or specific to justify its own file**, declare it as a **private widget** in the same file, below the parent widget it belongs to.

```dart
// course_list_tile.dart

class CourseListTile extends StatelessWidget {
  const CourseListTile({super.key, required this.data});
  final CourseListTileData data;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: _CourseAvatar(imageUrl: data.imageUrl),
      title: Text(data.title),
      subtitle: Text(data.subtitle),
    );
  }
}

// Private — too specific and small to justify its own file
class _CourseAvatar extends StatelessWidget {
  const _CourseAvatar({required this.imageUrl});
  final String imageUrl;

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(backgroundImage: NetworkImage(imageUrl));
  }
}
```

### 2.3 Widget Models (Data Classes)

- **Public widgets** that have **more than 2 non-action parameters** should receive their data through a dedicated immutable model. The parameter name is always `data`.
- **Private widgets** have no such restriction — they can take as many parameters as needed.
- If a parameter does not logically relate to the others, it does not need to be added to the model; it can remain a separate named parameter.
- **Screens/Views** passed to a `GoRoute` must **strictly** accept only one parameter, and that parameter must be a model.

```dart
// The model — immutable by default via dart_mappable
@MappableClass()
class ModuleListTileData with ModuleListTileDataMappable {
  final bool selected;
  final String title;
  final String subtitle;

  const ModuleListTileData({
    required this.selected,
    required this.title,
    required this.subtitle,
  });
}

// The widget
class ModuleListTile extends StatelessWidget {
  const ModuleListTile({super.key, required this.data});
  final ModuleListTileData data;

  @override
  Widget build(BuildContext context) { ... }
}

// Screen — strictly one model param
@MappableClass()
class CreateCourseViewData with CreateCourseViewDataMappable {
  final String? prefillTitle;
  const CreateCourseViewData({this.prefillTitle});
}

class CreateCourseView extends StatelessWidget {
  const CreateCourseView({super.key, required this.data});
  final CreateCourseViewData data;
  ...
}
```

### 2.4 Use Specialist Widgets Over Generalist Ones

Always prefer the most specific widget for the job. Avoid over-engineering with heavier widgets when lighter ones exist.

```dart
// Bad — Container just for a background color
Container(
  color: Colors.blue,
  child: child,
)

// Good
ColoredBox(
  color: Colors.blue,
  child: child,
)
```

Other examples:
- Use `SizedBox` for whitespace, not `Container`.
- Use `Padding` for padding only, not `Container`.
- Use `DecoratedBox` when you only need a decoration.
- Use `Align` instead of a `Center` + `Container` combination.

### 2.5 Prefer `dart_mappable` Over `freezed`

All data models use `dart_mappable`. Do not use `freezed`.

---

## 3. Code Documentation Standards

### 3.1 Simple Functions

A single-line triple-slash comment. Brief, concise, exactly describing what the function does.

```dart
/// Returns the formatted display name for the given user.
String getDisplayName(User user) => '${user.firstName} ${user.lastName}';
```

### 3.2 Complex Functions with Private Helpers

A complex function (one that calls private helper methods) gets:
1. A **3-line ASCII separator** above it.
2. A **one-liner triple-slash comment** on the line directly after the separator.
3. Its **private helper methods placed immediately below it**, before the next separator.

```dart
// ============================================================
// Processes and submits the course creation form
// ============================================================
/// Validates inputs, maps to query model, and delegates to logic.
Future<void> _processAndSubmitCourse() async {
  final validated = _validateInputs();
  if (!validated) return;
  final query = _buildQuery();
  await _submitQuery(query);
}

Future<bool> _validateInputs() async { ... }
CreateCourseQuery _buildQuery() { ... }
Future<void> _submitQuery(CreateCourseQuery query) async { ... }

// ============================================================
// Next major function group
// ============================================================
```

### 3.3 Class-Level Comments

Classes should have a brief doc comment explaining their purpose.

```dart
/// Manages all user-facing actions for the create course screen.
mixin CreateCourseActionsMixin on ... { }
```

---

## 4. Performance Optimization

- **`const` constructors everywhere possible.** If a widget's build output never changes, make it `const`.
- **Avoid rebuilding unchanged subtrees.** Pass only what each widget needs; do not expose the entire state object.
- **Use `RepaintBoundary`** to isolate expensive paint operations (e.g., animations, complex graphics) from the rest of the tree.
- **Lazy loading for lists.** Always use `ListView.builder` / `SliverList` with a delegate rather than building all children eagerly.
- **Offload heavy computation to isolates.** Use `compute()` or a dedicated `SmartIsolate` utility (see `lib/core/utils`) for CPU-bound tasks.
- **Image optimization.** Cache network images. Use appropriate resolution assets. Compress before uploading.
- **Minimize `setState` scope.** Call `setState` on the smallest widget that owns the state, not the root.

---

## 5. Folder Structure Overview

```
lib/
├── core/
│   ├── api/
│   ├── assets/
│   ├── base/
│   ├── constants/
│   ├── interop/
│   ├── notifiers/
│   ├── storage/
│   └── utils/
├── data/
│   ├── models/
│   │   ├── in/
│   │   └── out/
│   └── src/
└── features/
    └── <feature_name>/
        ├── ui/
        │   ├── actions/
        │   ├── models/
        │   ├── screens/
        │   └── widgets/
        ├── logic/
        └── providers/   ← or state/
```

Every folder (unless it is a title/organizer folder) follows this internal pattern:

```
<folder>/
├── src/           ← implementation files
├── models/        ← only if necessary
│   ├── in/
│   └── out/
├── extra/         ← only if necessary, for files that don't fit src or models
└── <folder>.dart  ← barrel/super file that exports everything above
```

---

## 6. lib/core

Core holds all foundational, app-wide infrastructure — things that are reused everywhere and have no dependency on features.

---

### 6.1 core/api

Abstracts all external API interactions.

```
core/api/
├── src/
│   ├── analysis_api.dart     // Groups related API calls into a class
│   └── auth_api.dart
├── models/
│   ├── in/                   // Response models from the backend
│   │   └── get_analysis_response.dart
│   └── out/                  // Request/query models sent to the backend
│       └── get_analysis_query.dart
├── api.dart                  // Top-level Api() class: Api.instance.analysis.analyzeData(data)
└── api_paths.dart            // All API endpoint path constants
```

**`api.dart`** — provides a unified access point:
```dart
class Api {
  static final Api instance = Api._();
  Api._();

  final AnalysisApi analysis = AnalysisApi();
  final AuthApi auth = AuthApi();
}
```

**`api_paths.dart`** — centralizes all endpoint strings:
```dart
abstract final class ApiPaths {
  static const String analyzeData = '/v1/analysis/analyze';
  static const String authVerify  = '/v1/auth/verify';
}
```

**`ApiCacheMixin`** — every API class that needs caching applies this mixin. Actual storage backend (Hive, Isar, etc.) is wired inside the mixin independently, keeping API classes clean:

```dart
mixin ApiCacheMixin {
  final Map<String, dynamic> _cacheMap = {};

  T? getCache<T>(String key) => _cacheMap[key] as T?;
  void setCache(String key, dynamic value) => _cacheMap[key] = value;
}

class AnalysisApi with ApiCacheMixin {
  // Cache key IDs declared neatly at class top
  static const _historyId = 'analysis_history';

  set history(List<AnalysisItem> value) => setCache(_historyId, value);
  List<AnalysisItem>? get history => getCache(_historyId);

  // ============================================================
  // Fetches analysis history, using cache when available
  // ============================================================
  /// Returns cached history or fetches from remote if stale.
  Future<Result<List<AnalysisItem>>> getHistory() async { ... }
}
```

**Model naming conventions:**
- Response (in) → `GetAnalysisResponse`, `AuthVerifyResponse`
- Query (out) → `GetAnalysisQuery`, `UpdateUserQuery`
- For responses relying on a single primitive value with no meaningful model, no model is needed.
- All API models implement `ApiResponse` for common fields (success flag, error message, etc.).
- JSON serialization is handled via `dart_mappable`. API fields use underscore; configure `dart_mappable` to handle snake_case↔camelCase mapping.

**Folder escalation rule:** if a specific API (e.g., `analysis_api`) grows large enough to need multiple files, create a sub-folder:
```
src/
└── analysis/
    ├── analysis_api.dart
    └── analysis_helpers.dart
```

---

### 6.2 core/assets

Managed by `assets_gen`. Running `build_runner` auto-generates the `gen/` files. Do not manually manage asset references — always use the generated accessors.

```
core/assets/
├── gen/           ← auto-generated by assets_gen + build_runner
└── assets.dart    ← barrel file
```

---

### 6.3 core/base

Holds reusable mixins and base classes that eliminate repetition across the app. All implementation files live inside `src/`.

```
core/base/
├── src/
│   ├── is_scrolled_state_mixin.dart
│   ├── scroll_offset_state_mixin.dart
│   └── ...
└── base.dart   ← barrel, same level as src/
```

```dart
/// Provides scroll controller and a notifier for tracking scroll state.
mixin IsScrolledStateMixin<T extends StatefulWidget> on State<T> {
  late final ScrollController scrollController = ScrollController();
  final ValueNotifier<bool> isScrolled = ValueNotifier(false);

  @override
  void initState() {
    super.initState();
    scrollController.addListener(_onScroll);
  }

  void _onScroll() {
    isScrolled.value = scrollController.offset > 0;
  }

  @override
  void dispose() {
    scrollController.dispose();
    isScrolled.dispose();
    super.dispose();
  }
}
```

---

### 6.4 core/constants

Holds app-wide constant values. Enums and any other values that qualify as constants live inside `src/`.

```
core/constants/
├── src/
│   ├── enums.dart
│   └── app_durations.dart
└── constants.dart   ← barrel; exports everything in src/
```

The barrel can use a `part` / `part of` pattern or standard exports — either way `constants.dart` is the single import point.

---

### 6.5 core/storage

Abstracts all local persistence drivers behind a unified `Storage` interface.

```
core/storage/
├── src/
│   ├── app_hive_data.dart
│   └── app_isar_data.dart
└── storage.dart   ← Storage singleton
```

```dart
class Storage {
  static final Storage instance = Storage._();
  Storage._();

  final AppHiveData hive = AppHiveData();
  final AppIsarData isar = AppIsarData();
}

// Usage anywhere in app:
// Storage.instance.hive.initialize()
// Storage.instance.isar.getBox('courses')
```

---

### 6.6 core/utilities

Granular utility files grouped by domain.

```
core/utils/
├── storage/
│   ├── file_utils.dart
│   └── clean_up_utils.dart
├── crypto_utils.dart
├── device_utils.dart
├── smart_isolate.dart
└── utils.dart   ← barrel
```

---

### 6.7 core/interop

Handles all interactions between the app and the host OS or external apps — deep links, file sharing, incoming/outgoing files, OS intents, etc.

```
core/interop/
├── src/
│   ├── deep_link_handler.dart
│   ├── file_receiver.dart
│   └── file_sender.dart
└── interop.dart
```

---

### 6.8 core/notifiers

App-wide `ValueNotifier` / `ChangeNotifier` instances that don't belong to any single feature — e.g., connectivity state, theme mode, locale.

```
core/notifiers/
├── src/
│   ├── connectivity_notifier.dart
│   └── theme_notifier.dart
└── notifiers.dart
```

---

## 7. lib/data

Holds all data-access repositories. Think of it as the implementation layer for structured data reads and writes, using the storage drivers from `core/storage`.

```
data/
├── models/
│   ├── in/
│   └── out/
├── src/
│   ├── course_repo.dart
│   └── user_repo.dart
└── data.dart
```

```dart
/// Handles all local read/write operations for course data.
class CourseRepo {
  final AppIsarData _isar = Storage.instance.isar;

  Future<Result<List<Course>>> getCourses() async { ... }
  Future<Result<void>> saveCourse(Course course) async { ... }
}
```

- Data access repos implement specific storage drivers (e.g., Isar, Hive) directly — no extra abstraction unless warranted.
- `models/in` and `models/out` follow the same conventions as in `core/api`.
- Architecture is open to future expansion.

---

## 8. lib/features

Each feature is a self-contained folder:

```
features/
└── course/
    ├── ui/
    │   ├── actions/
    │   ├── models/
    │   ├── screens/
    │   └── widgets/
    ├── logic/
    └── providers/
```

All three top-level folders (`ui`, `logic`, `providers`) are non-compulsory — only add what the feature actually needs.

---

### 8.1 UI Layer

#### screens/

Contains all screens for the feature. Always suffix with `View`, never `Screen`.

```
screens/
├── create_course_view.dart
└── course_detail_view.dart
```

#### actions/

Contains UI-layer action mixins — things that need `BuildContext`, `ref`, navigation, dialogs, snackbars, etc.

- Default: one file per screen — `create_course_actions.dart`.
- If a screen's actions are too large for one file, escalate to a folder:

```
actions/
└── create_course_actions/
    ├── create_course_submit_actions.dart
    └── create_course_nav_actions.dart
```

Actions are implemented as **mixins**:

```dart
/// Handles all user-triggered actions for the create course screen.
mixin CreateCourseActionsMixin {
  // For Riverpod — prefer ref over context; context is available via ref.context
  Future<void> onSubmitTapped(WidgetRef ref) async {
    final result = await ref.read(createCourseLogicProvider).submit();
    result.when(
      success: (_) => ref.context.pop(),
      failure: (e) => showErrorSnackbar(ref.context, e),
    );
  }
}
```

#### widgets/

Contains feature-specific widgets. If a screen's widgets are numerous, create a named sub-folder:

```
widgets/
├── course_list_tile.dart
└── create_course/
    ├── course_image_picker.dart
    └── course_title_field.dart
```

#### models/

UI-only models — not data-layer models. These are passed to widgets as the `data` parameter.

```dart
@MappableClass()
class CourseListTileData with CourseListTileDataMappable {
  final String title;
  final String subtitle;
  final bool isSelected;
  const CourseListTileData({...});
}
```

If models grow numerous, nest sub-folders here too. No `src/` or `models/` sub-pattern needed inside `ui/`.

---

### 8.2 Logic Layer

Contains all **non-UI business logic** — complex data transformations, multi-step workflows, repo interactions, etc. Nothing in `logic/` should reference `BuildContext` or Riverpod's `ref` (UI concerns belong in `actions/`).

```dart
/// Orchestrates course creation: validates, maps, and persists.
class CreateCourseLogic {
  final CourseRepo _repo;
  CreateCourseLogic(this._repo);

  // ============================================================
  // Submits a new course after validation and transformation
  // ============================================================
  /// Validates the input, builds the persistence model, and saves.
  Future<Result<void>> submit(CreateCourseInput input) async {
    final validated = _validate(input);
    if (validated.isFailure) return validated;
    final course = _map(input);
    return _repo.saveCourse(course);
  }

  bool _validate(CreateCourseInput input) { ... }
  Course _map(CreateCourseInput input) { ... }
}
```

**All logic methods return `Result<T>`.** Never throw from a logic class — wrap errors in the `Result` type.

---

### 8.3 Providers / State Layer

Named `providers/` when using Riverpod or Provider. Named `state/` otherwise.

See [Section 9](#9-riverpod-state-pattern) for the full Riverpod pattern.

---

## 9. Riverpod State Pattern

### 9.1 Registry Pattern

Each feature's notifiers are wired together through a central **registry notifier**. The registry is the single entry point for the feature's state from the UI.

```
providers/
├── course_providers.dart         ← registry / entry point
├── course_list_notifier.dart
└── course_detail_notifier.dart
```

```dart
// course_providers.dart — the registry
final courseProvidersProvider = Provider((ref) => CourseProviders(ref));

class CourseProviders {
  CourseProviders(this._ref);
  final Ref _ref;

  CourseListNotifier get list => _ref.read(courseListNotifierProvider.notifier);
  CourseDetailNotifier get detail => _ref.read(courseDetailNotifierProvider.notifier);
}
```

**Usage in UI:**
```dart
// Access state
final courses = ref.watch(courseListNotifierProvider);

// Trigger actions through registry
ref.read(courseProvidersProvider).list.load();
```

### 9.2 Notifier Scoping Escalation

- **Single notifier for a view** → one file inside `providers/`.
- **Multiple notifiers for a view** → create a named sub-folder for that view's notifiers:

```
providers/
├── course_providers.dart
└── library/
    ├── library_notifier.dart
    └── course_pagination_notifier.dart
```

### 9.3 Prefer `ref` Over `context` in Riverpod

Always use `ref` for state access. Use `ref.context` when the build context is actually needed (navigation, theming) rather than passing `context` explicitly.

### 9.4 Self-Contained Storage Providers

If a notifier manages its own storage (e.g., a settings notifier that reads/writes directly to Hive), that is fine — encapsulate it inside the notifier rather than routing through a repo unnecessarily.

### 9.5 Structural Precedence Rule

Before creating a new structural pattern in a feature, **check if any other feature has already solved the same structural problem**. If yes, mirror it. If no existing pattern applies, reason up a new one and apply it consistently going forward.

---

## 10. Shared Packages & Preferences

| Concern | Package |
|---|---|
| Data models / serialization | `dart_mappable` |
| State management | Riverpod (preferred) |
| Navigation | GoRouter |
| Asset generation | `assets_gen` + `build_runner` |
| Local storage | Hive / Isar (via `core/storage`) |

### General Preferences

- Prefer `dart_mappable` over `freezed` for all data classes.
- For Riverpod, prefer `ref` over `context`.
- Screens accept exactly **one model parameter**.
- Public widgets with more than 2 non-action parameters use a `data` model.
- Private widgets have no parameter restrictions.
- All logic methods return `Result<T>`.
- `const` constructors everywhere possible.
- `assets_gen` manages all asset references — never hardcode asset path strings.

---

> **Note to AI tooling:** Before generating any file or folder, verify the existing structure of the project and mirror established patterns. Only introduce new structural patterns when no existing precedent applies. All custom widgets defined in `lib/features` for later integration should be flagged for review with the developer before finalizing the blueprint.
Also, keep tracking in a cache_progress.md file in the project's root for changes you've made that might be beneficial to the next model. always make sure to update