import 'package:starlight/domain/models/misc/file_path.dart';
import 'package:starlight/shared/helpers/extensions/extensions.dart';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'dart:io';
import 'dart:typed_data';

import 'package:cached_network_image/cached_network_image.dart';

export 'package:starlight/domain/models/misc/file_path.dart';

int fileImageVersion(File file) {
  try {
    final stat = file.statSync();
    return Object.hash(stat.modified.millisecondsSinceEpoch, stat.size);
  } catch (_) {
    return file.path.hashCode;
  }
}

class _VersionedFileImage extends FileImage {
  const _VersionedFileImage(super.file, {super.scale = 1.0, required this.version});

  final Object version;

  @override
  bool operator ==(Object other) {
    return other is _VersionedFileImage &&
        other.file.path == file.path &&
        other.scale == scale &&
        other.version == version;
  }

  @override
  int get hashCode => Object.hash(file.path, scale, version);
}

class AdaptiveImage extends ConsumerStatefulWidget {
  final FilePath path;
  final Widget fallbackWidget;
  final BoxFit fit;
  final double? width;
  final double? height;
  const AdaptiveImage({
    super.key,
    required this.path,
    this.fallbackWidget = const Icon(Icons.image),
    this.fit = BoxFit.cover,
    this.width,
    this.height,
  });

  @override
  ConsumerState<ConsumerStatefulWidget> createState() => _AdaptiveImageState();
}

class _AdaptiveImageState extends ConsumerState<AdaptiveImage> {
  ///
  @override
  Widget build(BuildContext context) {
    final path = widget.path;
    final fallbackWidget = widget.fallbackWidget;
    final fit = widget.fit;
    final width = widget.width;
    final height = widget.height;
    final local = path.local;

    if (!path.containsAnyPath) return fallbackWidget;

    if (local != null && local.isNotEmpty) {
      // && imageBytes != null
      return ImageFromFile(
        fileDetails: path,
        fit: fit,
        width: width,
        height: height,
        fallbackWidget: fallbackWidget,
        ref: ref,
      ).animate().fadeIn();
    } else if (path.url != null) {
      return ImageFromNetwork(
        fileDetails: path,
        fit: fit,
        width: width,
        height: height,
        fallbackWidget: fallbackWidget,
      ).animate().fadeIn();
    }

    return fallbackWidget;
  }
}

class ImageFromFile extends StatelessWidget {
  const ImageFromFile({
    super.key,
    required this.fileDetails,
    required this.fit,
    required this.width,
    required this.height,
    required this.fallbackWidget,
    required this.ref,
  });

  final FilePath fileDetails;
  final BoxFit fit;
  final double? width;
  final double? height;
  final Widget fallbackWidget;
  final WidgetRef ref;

  @override
  Widget build(BuildContext context) {
    final imageFile = File(fileDetails.local ?? '');
    return Image(
      image: _VersionedFileImage(imageFile, version: fileImageVersion(imageFile)),
      fit: fit,
      width: width,
      height: height,
      errorBuilder: (context, error, stackTrace) => fallbackWidget,
      frameBuilder: (BuildContext context, Widget child, int? frame, bool wasSynchronouslyLoaded) {
        if (wasSynchronouslyLoaded || frame != null) {
          return child;
        } else {
          final theme = context.theme;
          return SizedBox.expand(child: ColoredBox(color: theme.primaryColor.withAlpha(40)))
              .animate(onInit: (controller) => controller.repeat())
              .shimmer(duration: const Duration(seconds: 1), curve: Curves.decelerate)
              .blurXY(begin: 2, end: 0, duration: Duration(seconds: 1))
              .animate(onComplete: (controller) => controller.repeat(reverse: true))
              .tint(color: theme.primaryColor.withAlpha(10), duration: Duration(seconds: 1));
        }
      },
    );
  }
}

class ImageFromNetwork extends StatelessWidget {
  const ImageFromNetwork({
    super.key,
    required this.fileDetails,
    required this.fit,
    required this.width,
    required this.height,
    required this.fallbackWidget,
  });

  final FilePath fileDetails;
  final BoxFit fit;
  final double? width;
  final double? height;
  final Widget fallbackWidget;

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: fileDetails.url ?? '',
      fit: fit,
      width: width,
      height: height,
      progressIndicatorBuilder: (context, url, progress) {
        final theme = context.theme;
        return SizedBox.expand(child: ColoredBox(color: theme.primaryColor.withAlpha(40)))
            .animate(onComplete: (controller) => controller.repeat())
            .shimmer(duration: const Duration(seconds: 1), curve: Curves.decelerate)
            .blurXY(begin: 2, end: 0, duration: Duration(seconds: 1))
            .animate(onComplete: (controller) => controller.repeat(reverse: true))
            .tint(color: theme.primaryColor.withAlpha(10), duration: Duration(seconds: 1));
      },
      errorWidget: (context, error, stackTrace) => fallbackWidget,
    );
  }
}

class ImageFromMemory extends ConsumerWidget {
  const ImageFromMemory({
    super.key,
    required this.imageBytes,
    required this.fit,
    required this.width,
    required this.height,
    required this.fallbackWidget,
  });

  final Uint8List? imageBytes;
  final BoxFit fit;
  final double? width;
  final double? height;
  final Widget fallbackWidget;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Image.memory(
      imageBytes!,
      fit: fit,
      width: width,
      height: height,
      frameBuilder: (BuildContext context, Widget child, int? frame, bool wasSynchronouslyLoaded) {
        if (wasSynchronouslyLoaded || frame != null) {
          return child;
        } else {
          final theme = context.theme;
          return SizedBox.expand(child: ColoredBox(color: theme.primaryColor.withAlpha(40)))
              .animate(onComplete: (controller) => controller.repeat())
              .shimmer(duration: const Duration(seconds: 1), curve: Curves.decelerate)
              .blurXY(begin: 2, end: 0, duration: Duration(seconds: 1))
              .animate(onComplete: (controller) => controller.repeat(reverse: true))
              .tint(color: theme.primaryColor.withAlpha(10), duration: Duration(seconds: 1));
        }
      },
      errorBuilder: (context, error, stackTrace) => fallbackWidget,
    );
  }
}
