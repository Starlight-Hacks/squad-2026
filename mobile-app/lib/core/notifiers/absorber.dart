import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_riverpod/misc.dart';

/// Use [ref.context] to access the [BuildContext context]
typedef AbsorbBuilder<OutT> = Widget Function(WidgetRef ref, OutT value, Widget? _);

class Absorb {
  static Widget watch<OutT>(
    ProviderListenable<OutT> listenable, {
    Key? key,
    required AbsorbBuilder<OutT> builder,
    Widget? child,
  }) => AbsorbWatch(key: key, listenable: listenable, builder: builder, child: child);

  static Widget read<OutT>(
    ProviderListenable<OutT> listenable, {
    Key? key,
    required AbsorbBuilder<OutT> builder,
    Widget? child,
  }) => AbsorbRead(key: key, listenable: listenable, builder: builder, child: child);

  // static Widget readValueNotifier<OutT>(
  //   ProviderListenable<ValueNotifier<OutT>> listenable, {
  //   Key? key,
  //   required AbsorberBuilder<OutT> builder,
  //   Widget? innerChild,
  //   Widget? outerChild,
  // }) {
  //   return AbsorberValueNotifier<OutT>(
  //     key: key,
  //     listenable: listenable,
  //     builder: builder,
  //     outerChild: outerChild,
  //     innerChild: innerChild,
  //     watchNotRead: false,
  //   );
  // }

  // static Widget watchValueNotifier<OutT>(
  //   ProviderListenable<ValueNotifier<OutT>> listenable, {
  //   Key? key,
  //   required AbsorberBuilder<OutT> builder,
  //   Widget? innerChild,
  //   Widget? outerChild,
  // }) {
  //   return AbsorberValueNotifier<OutT>(
  //     key: key,
  //     listenable: listenable,
  //     builder: builder,
  //     outerChild: outerChild,
  //     innerChild: innerChild,
  //     watchNotRead: true,
  //   );
  // }
}

/// Watches the Provider supplied
class AbsorbWatch<OutT> extends ConsumerWidget {
  final ProviderListenable<OutT> listenable;
  final AbsorbBuilder<OutT> builder;
  final Widget? child;
  const AbsorbWatch({super.key, required this.listenable, required this.builder, this.child});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(listenable);
    return builder(ref, value, child);
  }
}

/// Reads the Provider supplied
class AbsorbRead<OutT> extends ConsumerWidget {
  final ProviderListenable<OutT> listenable;
  final AbsorbBuilder<OutT> builder;
  final Widget? child;
  const AbsorbRead({super.key, required this.listenable, required this.builder, this.child});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.read(listenable);
    return builder(ref, value, child);
  }
}

// /// Reads or watches the Provider as ValueNotifier when supplied
// class AbsorberValueNotifier<OutT> extends ConsumerWidget {
//   final ProviderListenable<ValueNotifier<OutT>> listenable;
//   final AbsorberBuilder<OutT> builder;
//   final Widget? innerChild;
//   final Widget? outerChild;

//   /// Will [watch] when true, [read] when false
//   final bool watchNotRead;
//   const AbsorberValueNotifier({
//     super.key,
//     required this.listenable,
//     required this.builder,
//     this.innerChild,
//     this.outerChild,
//     this.watchNotRead = false,
//   });

//   @override
//   Widget build(BuildContext context, WidgetRef ref) {
//     if (watchNotRead) {
//       return AbsorberWatch<ValueNotifier<OutT>>(
//         listenable: listenable,
//         builder: (context, valueListenable, ref, child) => ValueListenableBuilder<OutT>(
//           valueListenable: valueListenable,
//           builder: (c, v, i) => builder(c, v, ref, i),
//           child: innerChild,
//         ),
//         child: outerChild,
//       );
//     }
//     return AbsorberRead<ValueNotifier<OutT>>(
//       listenable: listenable,
//       builder: (context, valueListenable, ref, child) => ValueListenableBuilder<OutT>(
//         valueListenable: valueListenable,
//         builder: (c, v, i) => builder(c, v, ref, i),
//         child: innerChild,
//       ),
//       child: outerChild,
//     );
//   }
// }
