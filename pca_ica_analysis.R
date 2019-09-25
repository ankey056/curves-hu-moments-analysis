


require(fastICA)


d <- read.table("./output/painted-contours-hu.dat",
                colClasses = c("character", "integer",
                               rep("double", 7),
                               "character"))

X <- as.matrix(d[2:9])


a <- fastICA(X, 2, # alg.typ = "deflation", 
             method = "R", row.norm = FALSE, maxit = 200,
             tol = 0.0001, verbose = TRUE)

pca <- a$X %*% a$K
ica <- a$S

Mica <- a$K %*% a$W
# Mica <-  a$W %*% a$K

write.table(cbind(pca, ica),
            file="./output/pca-ica-analysis.dat",
            row.names=FALSE, col.names=FALSE)

write.table(a$K,
            file="./output/pca-matrix.dat",
            row.names=FALSE, col.names=FALSE)

write.table(Mica,
            file="./output/ica-matrix.dat",
            row.names=FALSE, col.names=FALSE)
