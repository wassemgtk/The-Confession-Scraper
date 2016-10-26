#! /usr/bin/Rscript
args = commandArgs(trailingOnly=TRUE)

print('Done with converting file to matrix')
page_id <- args[1]
output <- args[2]
posts_split <- args[3]
matrix <- args[4]
print(page_id)
print(output)
print(posts_split)
print(matrix)

path <- file.path("..", "data", output)
# print(path)
page_id <- list.files(file.path(path, posts_split))
page_id.files <- file.path(path, posts_split, page_id)
# print(page_id.files)
all.files <- c(page_id.files)
txt <- lapply(all.files, readLines)
# string <- stringmerge("..", "..", "data", output, posts_split)
string <- paste(c("../", "data/", output, "/", posts_split), collapse='')
nms <- gsub(string, "", all.files)
data <- setNames(txt, nms)
data <- sapply(data, function(x) paste(x, collapse = " "))

filename <- paste(c("../", "data/", output, "/", matrix), collapse='')

# filename <- stringmerge("..", "..", "data", output, posts_split, matrix)
save(data, file = filename, compress = "xz") 