// ignore_for_file: public_member_api_docs, sort_constructors_first

class FilePath {
  final String? url;
  final String? local;

  const FilePath({this.url, this.local});

  factory FilePath.empty() => FilePath(url: '', local: '');

  FilePath copyWith({String? url, String? local}) {
    return FilePath(url: url ?? this.url, local: local ?? this.local);
  }

  @override
  bool operator ==(covariant FilePath other) {
    if (identical(this, other)) return true;

    return other.url == url && other.local == local;
  }

  @override
  int get hashCode => url.hashCode ^ local.hashCode;
}

extension FilePathExtension on FilePath {
  bool get containsLocalPath => (local != null && local!.trim().isNotEmpty);
  bool get containsUrlPath => (url != null && url!.trim().isNotEmpty);
  bool get containsAnyPath => containsLocalPath || containsUrlPath;
}
